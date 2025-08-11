import json
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import torch

def calculate_f1_score(precision, recall):
    """Calculate F1-score from precision and recall"""
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)

def get_detailed_metrics_from_results(results_json_path):
    """Extract detailed metrics from YOLOv8 results JSON file"""
    
    try:
        with open(results_json_path, 'r') as f:
            data = json.load(f)
        
        # Extract metrics from the JSON
        metrics = {}
        if 'metrics/precision(B)' in data:
            metrics['precision'] = data['metrics/precision(B)']
        if 'metrics/recall(B)' in data:
            metrics['recall'] = data['metrics/recall(B)']
        if 'metrics/mAP50(B)' in data:
            metrics['mAP50'] = data['metrics/mAP50(B)']
        if 'metrics/mAP50-95(B)' in data:
            metrics['mAP50_95'] = data['metrics/mAP50-95(B)']
            
        return metrics
    except FileNotFoundError:
        print(f"Results JSON file not found: {results_json_path}")
        return None

def evaluate_model_detailed(model_path, dataset_yaml_path):
    """Perform detailed evaluation and calculate all metrics"""
    
    print("Loading model for detailed evaluation...")
    model = YOLO(model_path)
    
    # Run validation to get detailed results
    results = model.val(
        data=dataset_yaml_path,
        split='test',  # Use test split
        save_json=True,
        conf=0.25,     # Confidence threshold
        iou=0.45,      # IoU threshold for NMS
        plots=True,
        verbose=True
    )
    
    print("\n" + "="*60)
    print("DETAILED MODEL EVALUATION RESULTS")
    print("="*60)
    
    # Overall metrics
    print(f"\nOVERALL METRICS:")
    print(f"{'Metric':<25} {'Value':<10}")
    print("-" * 40)
    print(f"{'mAP@0.5':<25} {results.box.map50:.4f}")
    print(f"{'mAP@0.75':<25} {getattr(results.box, 'map75', 'N/A') if hasattr(results.box, 'map75') else 'N/A'}")
    print(f"{'mAP@0.5:0.95':<25} {results.box.map:.4f}")
    print(f"{'Mean Precision':<25} {results.box.mp:.4f}")
    print(f"{'Mean Recall':<25} {results.box.mr:.4f}")
    print(f"{'Number of Classes':<25} {len(model.names)}")
    print(f"{'Number of Images':<25} {results.box.seen if hasattr(results.box, 'seen') else 'N/A'}")
    # Calculate overall F1-score
    overall_f1 = calculate_f1_score(results.box.mp, results.box.mr)
    print(f"{'Overall F1-Score':<25} {overall_f1:.4f}")

    # Print confusion matrix if available
    if hasattr(results, 'confusion_matrix') and results.confusion_matrix is not None:
        print("\nCONFUSION MATRIX:")
        print(results.confusion_matrix)
    
    # Per-class metrics
    print(f"\nPER-CLASS METRICS:")
    print(f"{'Class':<25} {'Precision':<10} {'Recall':<8} {'mAP50':<8} {'mAP50-95':<10} {'F1':<8} {'Samples':<8}")
    print("-" * 90)
    class_names = model.names
    per_class_metrics = []
    if hasattr(results.box, 'p') and hasattr(results.box, 'r') and hasattr(results.box, 'ap'):
        precisions = results.box.p
        recalls = results.box.r
        ap50s = results.box.ap50 if hasattr(results.box, 'ap50') else [0]*len(class_names)
        ap5095s = results.box.ap if hasattr(results.box, 'ap') else [0]*len(class_names)
        for i, class_name in enumerate(class_names.values()):
            precision = precisions[i] if i < len(precisions) else 0
            recall = recalls[i] if i < len(recalls) else 0
            ap50 = ap50s[i] if i < len(ap50s) else 0
            ap5095 = ap5095s[i] if i < len(ap5095s) else 0
            f1 = calculate_f1_score(precision, recall)
            num_targets = results.box.nt_per_class[i] if hasattr(results.box, 'nt_per_class') else 0
            print(f"{class_name:<25} {precision:.4f}    {recall:.4f}   {ap50:.4f}   {ap5095:.4f}   {f1:.4f}   {num_targets}")
            per_class_metrics.append({
                'class': class_name,
                'precision': precision,
                'recall': recall,
                'mAP50': ap50,
                'mAP50-95': ap5095,
                'f1': f1,
                'num_targets': num_targets
            })
    
    # Class distribution analysis
    print(f"\nCLASS DISTRIBUTION ANALYSIS:")
    print("-" * 40)
    if hasattr(results.box, 'nt_per_class'):
        total_instances = sum(results.box.nt_per_class)
        for i, class_name in enumerate(class_names.values()):
            num_instances = results.box.nt_per_class[i]
            percentage = (num_instances / total_instances) * 100 if total_instances > 0 else 0
            print(f"{class_name:<25} {num_instances:>6} ({percentage:>5.1f}%)")
    
    # Performance analysis
    print(f"\nPERFORMANCE ANALYSIS:")
    print("-" * 30)
    
    # Find best and worst performing classes
    if per_class_metrics:
        best_class = max(per_class_metrics, key=lambda x: x['f1'])
        worst_class = min(per_class_metrics, key=lambda x: x['f1'])
        
        print(f"Best performing class:  {best_class['class']} (F1: {best_class['f1']:.4f})")
        print(f"Worst performing class: {worst_class['class']} (F1: {worst_class['f1']:.4f})")
    
    # Speed metrics
    if hasattr(results, 'speed'):
        speed = results.speed
        print(f"\nSPEED METRICS:")
        print("-" * 20)
        print(f"Preprocess:  {speed['preprocess']:.1f}ms per image")
        print(f"Inference:   {speed['inference']:.1f}ms per image")
        print(f"Postprocess: {speed['postprocess']:.1f}ms per image")
        print(f"Total:       {sum(speed.values()):.1f}ms per image")
        print(f"FPS:         {1000/sum(speed.values()):.1f}")
    
    return results, per_class_metrics

def calculate_confusion_matrix_metrics(model_path, dataset_yaml_path):
    """Calculate accuracy using confusion matrix approach"""
    
    model = YOLO(model_path)
    
    # Get predictions on test set
    results = model.val(
        data=dataset_yaml_path,
        split='test',
        save_json=True,
        plots=False
    )
    
    # Note: YOLOv8 doesn't directly provide confusion matrix for object detection
    # because it's more complex than classification (involves IoU matching)
    print("\nNote: Accuracy calculation for object detection is complex")
    print("because it requires IoU-based matching between predictions and ground truth.")
    print("The mAP metrics are more appropriate for object detection tasks.")
    
    return results

if __name__ == "__main__":
    # Update these paths to match your setup
    MODEL_PATH = "runs_1\detect\cell-balance-augmented\weights\\best.pt"
    DATASET_YAML = "yolo_dataset/dataset.yaml"
    
    # Check if model exists
    if not Path(MODEL_PATH).exists():
        print(f"Model not found at: {MODEL_PATH}")
        print("Please check the path and make sure training completed successfully.")
        exit(1)
    
    # Perform detailed evaluation
    results, per_class_metrics = evaluate_model_detailed(MODEL_PATH, DATASET_YAML)
    
    # Calculate additional metrics if possible
    confusion_results = calculate_confusion_matrix_metrics(MODEL_PATH, DATASET_YAML)
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print("Key findings:")
    print("- mAP50 is the primary metric for object detection")
    print("- F1-scores calculated from precision and recall")
    print("- Check class distribution for potential data imbalance")
    print("- Consider data augmentation for poorly performing classes")
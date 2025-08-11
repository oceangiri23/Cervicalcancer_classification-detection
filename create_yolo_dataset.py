import os
import shutil
from pathlib import Path
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

def read_dat_file(dat_path):
    """Read coordinate data from .dat file"""
    coordinates = []
    with open(dat_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and ',' in line:
                try:
                    x, y = map(float, line.split(','))
                    coordinates.append([x, y])
                except ValueError:
                    continue
    return np.array(coordinates)

def polygon_to_bbox(coordinates):
    """Convert polygon coordinates to bounding box (x_min, y_min, x_max, y_max)"""
    if len(coordinates) == 0:
        return None
    
    x_coords = coordinates[:, 0]
    y_coords = coordinates[:, 1]
    
    x_min, x_max = np.min(x_coords), np.max(x_coords)
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    
    return x_min, y_min, x_max, y_max

def bbox_to_yolo_format(bbox, img_width, img_height):
    """Convert bounding box to YOLO format (normalized center_x, center_y, width, height)"""
    x_min, y_min, x_max, y_max = bbox
    
    # Calculate center coordinates and dimensions
    center_x = (x_min + x_max) / 2.0
    center_y = (y_min + y_max) / 2.0
    width = x_max - x_min
    height = y_max - y_min
    
    # Normalize by image dimensions
    center_x /= img_width
    center_y /= img_height
    width /= img_width
    height /= img_height
    
    return center_x, center_y, width, height

def create_yolo_dataset(archive_path, output_path):
    """Convert the dataset to YOLO format"""
    
    # Define class mapping
    class_names = [
        'Dyskeratotic',
        'Koilocytotic', 
        'Metaplastic',
        'Parabasal',
        'Superficial-Intermediate'
    ]
    
    class_mapping = {name: idx for idx, name in enumerate(class_names)}
    
    # Create output directory structure
    output_path = Path(output_path)
    images_dir = output_path / 'images'
    labels_dir = output_path / 'labels'
    
    for split in ['train', 'val', 'test']:
        (images_dir / split).mkdir(parents=True, exist_ok=True)
        (labels_dir / split).mkdir(parents=True, exist_ok=True)
    
    all_image_paths = []
    all_label_data = []
    
    # Process each class folder
    archive_path = Path(archive_path)
    for class_folder in archive_path.iterdir():
        if not class_folder.is_dir() or not class_folder.name.startswith('im_'):
            continue
            
        # Extract class name (remove 'im_' prefix)
        class_name = class_folder.name[3:]  # Remove 'im_' prefix
        if class_name not in class_mapping:
            print(f"Warning: Unknown class {class_name}")
            continue
            
        class_id = class_mapping[class_name]
        print(f"Processing class: {class_name} (ID: {class_id})")
        
        # Find all BMP images in this folder
        bmp_files = list(class_folder.glob('*.bmp'))
        
        for bmp_file in bmp_files:
            image_name = bmp_file.stem  # e.g., '001'
            
            # Read image to get dimensions
            img = cv2.imread(str(bmp_file))
            if img is None:
                print(f"Could not read image: {bmp_file}")
                continue
                
            img_height, img_width = img.shape[:2]
            
            # Find all cytoplasm files for this image
            cyt_files = list(class_folder.glob(f'{image_name}_cyt*.dat'))
            
            if not cyt_files:
                print(f"No cytoplasm files found for {bmp_file}")
                continue
            
            yolo_annotations = []
            
            # Process each cytoplasm (cell) in the image
            for cyt_file in cyt_files:
                coordinates = read_dat_file(cyt_file)
                
                if len(coordinates) < 3:  # Need at least 3 points for a polygon
                    continue
                
                # Convert polygon to bounding box
                bbox = polygon_to_bbox(coordinates)
                if bbox is None:
                    continue
                
                # Convert to YOLO format
                yolo_bbox = bbox_to_yolo_format(bbox, img_width, img_height)
                
                # Create YOLO annotation line: class_id center_x center_y width height
                yolo_line = f"{class_id} {yolo_bbox[0]:.6f} {yolo_bbox[1]:.6f} {yolo_bbox[2]:.6f} {yolo_bbox[3]:.6f}"
                yolo_annotations.append(yolo_line)
            
            if yolo_annotations:
                all_image_paths.append(str(bmp_file))
                all_label_data.append('\n'.join(yolo_annotations))
    
    print(f"Total images processed: {len(all_image_paths)}")
    
    # Split dataset into train/val/test
    train_imgs, temp_imgs, train_labels, temp_labels = train_test_split(
        all_image_paths, all_label_data, test_size=0.3, random_state=42, stratify=None
    )
    
    val_imgs, test_imgs, val_labels, test_labels = train_test_split(
        temp_imgs, temp_labels, test_size=0.5, random_state=42
    )
    
    splits = {
        'train': (train_imgs, train_labels),
        'val': (val_imgs, val_labels), 
        'test': (test_imgs, test_labels)
    }
    
    # Copy images and create label files
    for split_name, (img_paths, label_data) in splits.items():
        print(f"Creating {split_name} split with {len(img_paths)} images")
        
        for img_path, labels in zip(img_paths, label_data):
            img_path = Path(img_path)
            
            # Copy image
            dst_img_path = images_dir / split_name / img_path.name
            shutil.copy2(img_path, dst_img_path)
            
            # Create label file
            label_filename = img_path.stem + '.txt'
            dst_label_path = labels_dir / split_name / label_filename
            
            with open(dst_label_path, 'w') as f:
                f.write(labels)
    
    # Create dataset.yaml file
    yaml_content = f"""path: {output_path.absolute()}
train: images/train
val: images/val
test: images/test

nc: {len(class_names)}
names: {class_names}
"""
    
    with open(output_path / 'dataset.yaml', 'w') as f:
        f.write(yaml_content)
    
    print(f"\nDataset created successfully!")
    print(f"Classes: {class_names}")
    print(f"Train: {len(train_imgs)} images")
    print(f"Val: {len(val_imgs)} images") 
    print(f"Test: {len(test_imgs)} images")
    print(f"Dataset config saved to: {output_path / 'dataset.yaml'}")

# Usage example
if __name__ == "__main__":
    # Set your paths here
    archive_path = "archive"  # Path to your archive folder
    output_path = "yolo_dataset"           # Where to save the YOLO dataset
    
    create_yolo_dataset(archive_path, output_path)
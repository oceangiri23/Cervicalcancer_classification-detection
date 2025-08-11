from ultralytics import YOLO
import cv2
import os
import uuid
from pathlib import Path


def detection(image_path):
    model_path = 'best.pt'  # Change if needed

    UPLOAD_DIR = Path('results')  # Changed to static directory
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    file_extension = '.jpg'
    unique_filename = f"output_{uuid.uuid4()}{file_extension}"
    output_path = UPLOAD_DIR / unique_filename

    # ==== CHECK PATHS ====
    if not os.path.exists(model_path):
        print(f"Model not found at: {model_path}")
        return

    if not os.path.exists(image_path):
        print(f"Image not found at: {image_path}")
        return

    # ==== LOAD MODEL ====
    model = YOLO(model_path)

    # ==== RUN INFERENCE ====
    results = model(image_path)

    # ==== SAVE RESULT IMAGE ====
    result = results[0]
    result.save(filename=output_path)
    print(f"\nSaved result image to: {output_path}")

    # ==== PRINT DETECTIONS ====
    print(f"\nDetections for {image_path}:")
    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]
        print(f" - {label}: {conf:.2f}")

    # Return full URL that frontend can access
    return {
        "image_url": f"http://localhost:8000/results/{unique_filename}",
        "detections": [
            {"label": model.names[int(box.cls[0])],
             "confidence": float(box.conf[0])}
            for box in result.boxes
        ]
    }


# Remove or comment out the test code
# image_path = 'Sample_dataset/im_Dyskeratotic/001.bmp'
# detection(image_path)

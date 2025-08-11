from ultralytics import YOLO

def main():
    model = YOLO('yolov8s.pt')  # smaller model to reduce overfitting

    model.train(
        data='yolo_dataset/dataset.yaml',
        imgsz=640,
        epochs=150,
        batch=8,
        device=0,
        project='whole_data',
        name='cell-balance-augmented',

        # Optimizer
        optimizer='AdamW',
        lr0=0.001,
        lrf=0.01,
        weight_decay=0.0005,
        momentum=0.937,

        # Loss Weights
        box=7.0,
        cls=1.0,
        dfl=1.5,

        # Augmentation Tweaks
        scale=0.5,
        fliplr=0.75,
        mosaic=0.5,
        mixup=0.1,
        hsv_h=0.05,
        hsv_s=0.7,
        hsv_v=0.6,

        # Regularization
        label_smoothing=0.1,

        # Training Behavior
        patience=20,
        workers=4,
        pretrained=True,
        verbose=True,
        save=True,
        save_period=10
    )

if __name__ == "__main__":
    main()

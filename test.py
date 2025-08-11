from ultralytics import YOLO
import cv2

# Load model and image
model = YOLO("runs_1\detect\cell-balance-augmented\weights\\best.pt")
results = model("yolo_dataset\images\\test\\009.bmp")
# Plot results manually
result = results[0]
img_with_boxes = result.plot(line_width=3, font_size=1)  # Smaller font

# Show image using OpenCV
img_scaled = cv2.resize(img_with_boxes, (1280, 720))
cv2.imshow("YOLOv8 Detections", img_scaled)
cv2.waitKey(0)
cv2.destroyAllWindows()

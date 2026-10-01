from ultralytics import YOLO
import cv2
import os

# ==============================
# Load trained model
# ==============================
model = YOLO("best.pt")

# ==============================
# Read image
# ==============================
image_path = r"C:\games\Emergencies\dataset\test\images\WEB11690.jpg"      # Replace with your image
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
    exit()

# ==============================
# Run detection
# ==============================
results = model.predict(
    source=image,
    conf=0.30,
    imgsz=640,
    verbose=False
)

result = results[0]
annotated = result.plot()

# ==============================
# Check detections
# ==============================
danger = False
detected_classes = []

for box in result.boxes:
    cls = int(box.cls[0])
    conf = float(box.conf[0])

    class_name = model.names[cls]
    detected_classes.append(class_name)

    print(f"{class_name} detected ({conf:.2f})")

    if class_name in ["fire", "smoke"]:
        danger = True

# ==============================
# Display warning
# ==============================
if danger:

    if "fire" in detected_classes and "smoke" in detected_classes:
        message = "DANGER! FIRE & SMOKE DETECTED"

    elif "fire" in detected_classes:
        message = "DANGER! FIRE DETECTED"

    else:
        message = "WARNING! SMOKE DETECTED"

    cv2.putText(
        annotated,
        message,
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

# ==============================
# Detection count
# ==============================
cv2.putText(
    annotated,
    f"Detections: {len(result.boxes)}",
    (20, 90),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 0),
    2
)

# ==============================
# Save output image
# ==============================
output_path = "output_detection.jpg"
cv2.imwrite(output_path, annotated)

print(f"\nOutput saved as: {os.path.abspath(output_path)}")

# ==============================
# Show image
# ==============================
cv2.imshow("Fire & Smoke Detection System", annotated)

cv2.waitKey(0)
cv2.destroyAllWindows()
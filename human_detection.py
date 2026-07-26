from ultralytics import YOLO
import cv2
import os


# Load YOLOv8 pretrained model

model = YOLO("yolov8s.pt")   # COCO model


# Read image

image_path = r"C:\games\Emergencies\dataset\test\images\LDN-L-FILM-FIRESAFETY-1108-01-SR-1.webp"      # Replace with your image

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()


# Detect persons only

results = model.predict(
    source=image,
    classes=[0],      # COCO class 0 = Person
    conf=0.35,
    imgsz=640,
    verbose=False
)

result = results[0]

person_count = 0


# Draw detections

for box in result.boxes:

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    confidence = float(box.conf[0])

    person_count += 1

    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Person {confidence:.2f}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


# Display total people

cv2.putText(
    image,
    f"People Detected: {person_count}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    3
)


# Save result

output_path = "human_detection_output.jpg"

cv2.imwrite(output_path, image)

print(f"People detected: {person_count}")
print(f"Saved to: {os.path.abspath(output_path)}")


# Show image

cv2.imshow("Human Detection", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
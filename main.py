from ultralytics import YOLO
from danger_analyzer import DangerAnalyzer
import cv2


# Load Models


fire_model = YOLO(r"C:\games\Emergencies\runs\detect\train-6\weights\best.pt")
human_model = YOLO("yolov8n.pt")

analyzer = DangerAnalyzer()


# Read Image


image_path = r"C:\games\Emergencies\dataset\test\images\LDN-L-FILM-FIRESAFETY-1108-01-SR-1.webp"      # Change to your image

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

annotated = image.copy()


# Fire & Smoke Detection


fire_results = fire_model(image, conf=0.30)

fire_count = 0
smoke_count = 0

for box in fire_results[0].boxes:

    cls = int(box.cls[0])

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    if cls == 0:
        smoke_count += 1
        color = (0,255,255)
        label = "Smoke"

    else:
        fire_count += 1
        color = (0,0,255)
        label = "Fire"

    cv2.rectangle(annotated,(x1,y1),(x2,y2),color,2)

    cv2.putText(
        annotated,
        label,
        (x1,y1-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
    )


# Human Detection


human_results = human_model(image, conf=0.40)

people_count = 0

for box in human_results[0].boxes:

    cls = int(box.cls[0])

    # COCO class 0 = person
    if cls != 0:
        continue

    people_count += 1

    x1,y1,x2,y2 = map(int, box.xyxy[0])

    cv2.rectangle(
        annotated,
        (x1,y1),
        (x2,y2),
        (0,255,0),
        2
    )

    cv2.putText(
        annotated,
        "Person",
        (x1,y1-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,0),
        2
    )


# Danger Analysis


level, color = analyzer.analyze(
    fire_count,
    smoke_count,
    people_count
)

annotated = analyzer.draw_panel(
    annotated,
    fire_count,
    smoke_count,
    people_count,
    level,
    color
)


# Extra Warning


if fire_count > 0 or smoke_count > 0:

    cv2.putText(
        annotated,
        "DANGER DETECTED!",
        (30,230),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        3
    )


# Show Image


cv2.imshow("Smart Building Monitoring System", annotated)

cv2.waitKey(0)

cv2.destroyAllWindows()
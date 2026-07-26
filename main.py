from ultralytics import YOLO
import cv2

from danger_analyzer import DangerAnalyzer


# Load Models


fire_model = YOLO(r"C:\games\Emergencies\runs\detect\train-6\weights\best.pt")   # Change to your model path
person_model = YOLO("yolov8n.pt")                 # COCO model

danger = DangerAnalyzer()


# Detection Function


def process_frame(frame):

    fire_results = fire_model(frame, conf=0.35, verbose=False)
    person_results = person_model(frame, classes=[0], conf=0.40, verbose=False)

    annotated = frame.copy()

    # Draw fire/smoke detections
    annotated = fire_results[0].plot(img=annotated)

    fire_count = 0
    smoke_count = 0

    for box in fire_results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:
            smoke_count += 1

        elif cls == 1:
            fire_count += 1

    # Draw people
    people_count = 0

    for box in person_results[0].boxes:

        people_count += 1

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cv2.rectangle(annotated,
                      (x1, y1),
                      (x2, y2),
                      (0,255,0),
                      2)

        cv2.putText(annotated,
                    "Person",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2)

    level, color = danger.analyze(
        fire_count,
        smoke_count,
        people_count
    )

    annotated = danger.draw_panel(
        annotated,
        fire_count,
        smoke_count,
        people_count,
        level,
        color
    )

    return annotated


# Image Mode


def image_mode():

    image_path = input("Image path: ")

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found.")
        return

    result = process_frame(image)

    cv2.imshow("Smart Building Monitor", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Camera Mode


def camera_mode():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found.")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        result = process_frame(frame)

        cv2.imshow("Smart Building Monitor", result)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Main Menu


print(" SMART BUILDING SYSTEM")
print("1 - Test Image")
print("2 - Live Camera")

choice = input("Choose mode: ")

if choice == "1":
    image_mode()

elif choice == "2":
    camera_mode()

else:
    print("Invalid choice.")
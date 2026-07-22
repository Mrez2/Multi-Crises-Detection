from ultralytics import YOLO

def main():
    model = YOLO("yolov8s.pt")

    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        workers=8,
        cache=True,
        amp=True,
        device=0
    )

if __name__ == "__main__":
    main()
import torch
from ultralytics import YOLO

def main():
    model = YOLO("yolov8s.pt")

    model.train(
        data="Data/data.yaml",
        epochs=20,
        imgsz=640,
        batch=8,
        workers=2,
        cache=True,
        amp=True,
        device= "cpu",
    )

if __name__ == "__main__":
    main()
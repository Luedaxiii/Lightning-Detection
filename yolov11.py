from ultralytics import YOLO

def continue_training():
    # Load the best model from previous training
    model = YOLO("runs/detect/train24/weights/best.pt")

    # Continue training for 200 more epochs
    model.train(
        data='lightning2.yaml',  # Path to your dataset configuration file
        epochs=200,              # Number of additional epochs
        imgsz=640,               # Image size for training
        save_period=10           # Optional: save model every 10 epochs (adjust as needed)
    )

if __name__ == "__main__":
    continue_training()

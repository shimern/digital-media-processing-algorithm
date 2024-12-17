import cv2
from huggingface_hub import hf_hub_download
import time
from ultralytics import YOLO


def yolo_hg_face_detection():
    model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
    model = YOLO(model_path)
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame, stream=True)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Координаты рамки
                conf = box.conf[0]  # Уверенность
                label = f"Face: {conf:.2f}"
                # Отрисовка рамки и метки
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('YOLO Face Detection', frame)
        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # Освобождение ресурсов
    end_time = time.time()

    print(f"Время работы метода: {end_time - start_time:.5f} секунд")
    print(f"Скорость обработки: {cap.get(cv2.CAP_PROP_FPS):.0f} fps")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    yolo_hg_face_detection()
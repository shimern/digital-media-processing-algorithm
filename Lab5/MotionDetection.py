import cv2
import numpy as np

def GaussBlur(frame, k_size, deviation):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(img, (k_size, k_size), deviation)

def motion_detection(kernel_size=5,
                     deviation=5,
                     delta_tresh=25,
                     min_contour_area=500,
                     output_file='motion_detected.mp4',
                     input_file="./LR5/LR5_main_video.mov"):
    # Захват видео
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Не удалось открыть входной файл.")
        return

    # Подготовка видеофайла для записи
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для записи
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height), isColor=True)

    # Чтение первого кадра
    ret, frame = cap.read()
    if not ret:
        print("Не удалось прочитать первый кадр.")
        return

    old_frame = GaussBlur(frame, kernel_size, deviation)

    while True:
        ret, frame = cap.read()  # Чтение следующего кадра
        if not ret:  # Проверка успешности чтения
            break

        new_frame = GaussBlur(frame, kernel_size, deviation)

        # Вычисление разницы между кадрами
        frame_diff = cv2.absdiff(old_frame, new_frame)

        # Применение порогового преобразования
        _, thresh = cv2.threshold(frame_diff, delta_tresh, 255, cv2.THRESH_BINARY)

        # Нахождение контуров
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > min_contour_area:
                motion_detected = True
                break

        # Если движение обнаружено, записываем обработанный кадр в выходной файл
        if motion_detected:
            out.write(frame)  # Записываем чёрно-белый кадр

        # # Отображение текущего кадра
        # cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Video', 640, 480)  # изменение размера окна
        # cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        old_frame = new_frame

    # Освобождение ресурсов
    cap.release()
    out.release()
    cv2.destroyAllWindows()


# kernel_size = 3
# standard_deviation = 50
# delta_tresh = 60
# min_area = 20
# motion_detection(kernel_size, standard_deviation, delta_tresh, min_area)

# kernel_size = 11
# standard_deviation = 70
# delta_tresh = 60
# min_area = 20
# motion_detection(kernel_size, standard_deviation, delta_tresh, min_area)

# kernel_size = 3
# standard_deviation = 50
# delta_tresh = 20
# min_area = 20
# motion_detection(kernel_size, standard_deviation, delta_tresh, min_area)

# как по мне, более оптимальное
kernel_size = 3
standard_deviation = 50
delta_tresh = 60
min_area = 10
motion_detection(kernel_size, standard_deviation, delta_tresh, min_area)

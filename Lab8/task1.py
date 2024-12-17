import cv2  # OpenCV - библиотека для обработки изображений и видео
import time  # Библиотека для работы с временем

# Инициализация видеопотока с камеры (0 - это индекс устройства, обычно встроенная камера)
cap = cv2.VideoCapture(0)

# Загрузка классификатора Хаара для обнаружения лиц
# Файл с параметрами (каскадом Хаара) должен быть предварительно скачан и доступен по указанному пути
face_cascade = cv2.CascadeClassifier('sources_for_haarscade/haarcascade_frontalface_default.xml')

# Настройка параметров для записи видео
# fourcc - кодек для записи видео (XVID обеспечивает совместимость с AVI)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Создание объекта записи видео, который сохранит кадры в файл 'result/haarscade_output.avi'
# Параметры: имя файла, кодек, частота кадров, разрешение кадра (640x480)
out = cv2.VideoWriter('result/haarscade_output.avi', fourcc, 20.0, (640, 480))

# Переменные для подсчета частоты кадров (FPS) и времени между кадрами
frame_count = 0  # Счетчик обработанных кадров
prev_frame_time = 0  # Время последнего обновления кадра

# Запоминаем время начала выполнения программы
start_time = time.time()

# Основной цикл для захвата и обработки видеопотока
while True:
    # Захват кадра с камеры
    ret, frame = cap.read()  # ret - статус захвата (True/False), frame - текущий кадр

    # Проверяем, успешно ли захвачен кадр
    if ret:
        frame_count += 1  # Увеличиваем счетчик кадров

        # Получаем текущее время и разницу с предыдущим кадром
        current_time = time.time()
        time_diff = current_time - prev_frame_time

        # Преобразование кадра в оттенки серого для ускорения обработки
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Обнаружение лиц с использованием каскада Хаара
        # Параметры:
        # scaleFactor - во сколько уменьшается изображение на каждом масштабе
        # minNeighbors - количество соседних прямоугольников, необходимых для подтверждения лица
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Отрисовка прямоугольников вокруг обнаруженных лиц
        for (x, y, w, h) in faces:
            # Рисуем прямоугольник на кадре:
            # (x, y) - координаты верхнего левого угла, (x + w, y + h) - нижнего правого
            # Цвет - зеленый (0, 255, 0), толщина линии - 2 пикселя
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Сохраняем обработанный кадр в выходной видеопоток
        out.write(frame)

        # Вычисление частоты кадров (FPS) и вывод на экран
        if time_diff > 1:  # Обновляем FPS только раз в секунду
            fps = frame_count / time_diff  # FPS = количество кадров / время
            print(
                f"Частота потери изображения: {1 / ((current_time - prev_frame_time) / frame_count):.0f} кадр(-а)(-ов)/секунду"
            )
            prev_frame_time = current_time  # Обновляем время последнего кадра
            frame_count = 0  # Сбрасываем счетчик кадров

        # Отображение текущего кадра с прямоугольниками в окне 'Video'
        cv2.imshow('Video', frame)

        # Условие выхода из цикла: нажимаем 'Esc' (код 27) для остановки
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Запоминаем время окончания работы программы
end_time = time.time()

# Выводим время выполнения программы
print(f"Время работы метода: {end_time - start_time:.5f} секунд")

# Выводим скорость обработки кадров, запрашивая FPS с видеопотока
print(f"Скорость обработки: {cap.get(cv2.CAP_PROP_FPS):.0f} fps")

# Освобождение ресурсов камеры и объекта записи видео
cap.release()
out.release()

# Закрытие всех окон OpenCV
cv2.destroyAllWindows()

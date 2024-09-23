import cv2
import numpy as np


def web_video_to_hsv():
    #захват видео
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow("Web HSV", hsv_frame)  # Отображение кадра

        # Ожидание 20 мс и проверка нажатия клавиши 'Esc' (код 27)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()


    cv2.waitKey(0)

def filtering():
    # захват видео
    cap = cv2.VideoCapture(0)

    def nothing(args):
        pass

    # создаем окно для отображения результата и бегунки
    cv2.namedWindow("setup",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("setup", 300, 200)  # Изменяем размер окна управления
    cv2.createTrackbar("minH", "setup", 119, 179, nothing)
    cv2.createTrackbar("minS", "setup", 140, 255, nothing)
    cv2.createTrackbar("minV", "setup", 3, 255, nothing)
    cv2.createTrackbar("maxH", "setup", 137, 179, nothing)
    cv2.createTrackbar("maxS", "setup", 255, 255, nothing)
    cv2.createTrackbar("maxV", "setup", 255, 255, nothing)



    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        # собираем значения из бегунков в множества
        minH = cv2.getTrackbarPos('minH', 'setup')
        minS = cv2.getTrackbarPos('minS', 'setup')
        minV = cv2.getTrackbarPos('minV', 'setup')
        maxH = cv2.getTrackbarPos('maxH', 'setup')
        maxS = cv2.getTrackbarPos('maxS', 'setup')
        maxV = cv2.getTrackbarPos('maxV', 'setup')
        min_p = (minH, minS, minV)
        max_p = (maxH, maxS, maxV)


        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + 128) % 0xFF # смещение красного цвета в центр
        #чтобы не искать спектр мы его приведем в нужные значения самостоятельно

        # применяем фильтр, делаем бинаризацию
        mask = cv2.inRange(hsv_frame, min_p, max_p)


        hsv_frame_filtered = cv2.bitwise_and(frame, frame, mask=mask)  # создание фильтра
        cv2.imshow('Filtered Web Video', hsv_frame_filtered)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

def morphological_transformation():
    # захват видео
    cap = cv2.VideoCapture(0)

    def nothing(args):
        pass

    # создаем окно для отображения результата и бегунки
    cv2.namedWindow("setup",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("setup", 300, 200)  # Изменяем размер окна управления
    cv2.createTrackbar("minH", "setup", 119, 179, nothing)
    cv2.createTrackbar("minS", "setup", 140, 255, nothing)
    cv2.createTrackbar("minV", "setup", 3, 255, nothing)
    cv2.createTrackbar("maxH", "setup", 137, 179, nothing)
    cv2.createTrackbar("maxS", "setup", 255, 255, nothing)
    cv2.createTrackbar("maxV", "setup", 255, 255, nothing)



    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        # собираем значения из бегунков в множества
        minH = cv2.getTrackbarPos('minH', 'setup')
        minS = cv2.getTrackbarPos('minS', 'setup')
        minV = cv2.getTrackbarPos('minV', 'setup')
        maxH = cv2.getTrackbarPos('maxH', 'setup')
        maxS = cv2.getTrackbarPos('maxS', 'setup')
        maxV = cv2.getTrackbarPos('maxV', 'setup')
        min_p = (minH, minS, minV)
        max_p = (maxH, maxS, maxV)


        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + 128) % 0xFF # смещение красного цвета в центр
        #чтобы не искать спектр мы его приведем в нужные значения самостоятельно

        # применяем фильтр, делаем бинаризацию
        mask = cv2.inRange(hsv_frame, min_p, max_p)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5)))  # erosion + dilation (remove small objects)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5)))  # dilation + erosion (remove small holes)

        hsv_frame_filtered = cv2.bitwise_and(frame, frame, mask=mask)  # создание фильтра
        cv2.imshow('Filtered Web Video', hsv_frame_filtered)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

def find_moments():
    # захват видео
    cap = cv2.VideoCapture(0)

    def nothing(args):
        pass

    # создаем окно для отображения результата и бегунки
    cv2.namedWindow("setup",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("setup", 300, 200)  # Изменяем размер окна управления
    cv2.createTrackbar("minH", "setup", 119, 179, nothing)
    cv2.createTrackbar("minS", "setup", 140, 255, nothing)
    cv2.createTrackbar("minV", "setup", 3, 255, nothing)
    cv2.createTrackbar("maxH", "setup", 137, 179, nothing)
    cv2.createTrackbar("maxS", "setup", 255, 255, nothing)
    cv2.createTrackbar("maxV", "setup", 255, 255, nothing)



    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        # собираем значения из бегунков в множества
        minH = cv2.getTrackbarPos('minH', 'setup')
        minS = cv2.getTrackbarPos('minS', 'setup')
        minV = cv2.getTrackbarPos('minV', 'setup')
        maxH = cv2.getTrackbarPos('maxH', 'setup')
        maxS = cv2.getTrackbarPos('maxS', 'setup')
        maxV = cv2.getTrackbarPos('maxV', 'setup')
        min_p = (minH, minS, minV)
        max_p = (maxH, maxS, maxV)


        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + 128) % 0xFF # смещение красного цвета в центр
        #чтобы не искать спектр мы его приведем в нужные значения самостоятельно

        # применяем фильтр, делаем бинаризацию
        mask = cv2.inRange(hsv_frame, min_p, max_p)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5)))  # erosion + dilation (remove small objects)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5)))  # dilation + erosion (remove small holes)

        hsv_frame_filtered = cv2.bitwise_and(frame, frame, mask=mask)  # применение фильтра

        moments = cv2.moments(mask, True)
        print(moments['m00']) #вывод площади объекта

        cv2.imshow('Filtered Web Video', hsv_frame_filtered)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def build_a_contour():
    # захват видео
    cap = cv2.VideoCapture(0)

    def nothing(args):
        pass

    # создаем окно для отображения результата и бегунки
    cv2.namedWindow("setup",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("setup", 300, 200)  # Изменяем размер окна управления
    cv2.createTrackbar("minH", "setup", 119, 179, nothing)
    cv2.createTrackbar("minS", "setup", 140, 255, nothing)
    cv2.createTrackbar("minV", "setup", 3, 255, nothing)
    cv2.createTrackbar("maxH", "setup", 137, 179, nothing)
    cv2.createTrackbar("maxS", "setup", 255, 255, nothing)
    cv2.createTrackbar("maxV", "setup", 255, 255, nothing)



    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        # собираем значения из бегунков в множества
        minH = cv2.getTrackbarPos('minH', 'setup')
        minS = cv2.getTrackbarPos('minS', 'setup')
        minV = cv2.getTrackbarPos('minV', 'setup')
        maxH = cv2.getTrackbarPos('maxH', 'setup')
        maxS = cv2.getTrackbarPos('maxS', 'setup')
        maxV = cv2.getTrackbarPos('maxV', 'setup')
        min_p = (minH, minS, minV)
        max_p = (maxH, maxS, maxV)


        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + 128) % 0xFF # смещение красного цвета в центр
        #чтобы не искать спектр мы его приведем в нужные значения самостоятельно

        # применяем фильтр, делаем бинаризацию
        mask = cv2.inRange(hsv_frame, min_p, max_p)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((50, 50)))  # erosion и dilation : удаляем маленькие белые 7объекты
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((50, 50)))  # dilation и erosion : удаляем маленькие черные пробелы

        hsv_frame_filtered = cv2.bitwise_and(frame, frame, mask=mask)  # применение фильтра

# Почему изображение (маска) молучилось бинарным, если мы не вызывали соответствующую функцию?

        
        moments = cv2.moments(mask, True)
        print(moments['m00']) #вывод площади объекта

        m01 = moments['m01']  # Y
        m10 = moments['m10']  # X
        area = moments['m00']
        if area > 100:
            posX = int(m10 / area)
            posY = int(m01 / area)
            cv2.circle(frame, (posX, posY), 5, (255, 0, 0), -1)

            x, y, w, h = cv2.boundingRect(mask)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3)

        cv2.imshow('Filtered Web Video', hsv_frame_filtered)
        cv2.imshow('Web Video', frame)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()



web_video_to_hsv() #1
filtering() #2
morphological_transformation() #3
find_moments() #4
build_a_contour() #5




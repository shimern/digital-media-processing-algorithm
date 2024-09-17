#-*- coding: utf-8 -*-
#Задание 1 Установить библиотеку OpenCV.
from idlelib.colorizer import color_config

import cv2
import numpy as np

'''Задание 2 Вывести на экран изображение. Протестировать три
возможных расширения, три различных флага для создания окна и три
различных флага для чтения изображения.'''
def show_photo():
    cv2.namedWindow('Display window', cv2.WINDOW_AUTOSIZE)  # размер подгоняется под фотку
    img = cv2.imread('ferrari.jpg', 0)  # Загружает изображение в градациях серого (черно-белое).
    cv2.imshow('Display window', img)
    cv2.waitKey(0)

    cv2.namedWindow('Display window', cv2.WINDOW_NORMAL)  # Позволяет изменять размер окна вручную, фото растягивается
    img = cv2.imread('ferrari.jpg',-1)  # Загружает изображение с сохранением всех каналов, включая альфа-канал, если он есть.
    cv2.imshow('Display window', img)
    cv2.waitKey(0)

    cv2.namedWindow('Display window',cv2.WINDOW_KEEPRATIO)  # Сохраняет исходное соотношение сторон изображения при изменении размера окна
    img = cv2.imread('ferrari.jpg',1)  # Загружает цветное изображение по умолчанию. При этом все цветные каналы (BGR) сохраняются, но альфа-канал (прозрачность) игнорируется.
    cv2.imshow('Display window', img)
    cv2.waitKey(0)

'''Задание 3 Отобразить видео в окне. Рассмотреть методы класса
VideoCapture и попробовать отображать видео в разных форматах, в частности
размеры и цветовая гамма.'''

def print_info(cap):
    #Вывод информации о видео

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(width, height, fps)

def show_video():

    #захват видео
    cap = cv2.VideoCapture(r'C:\Users\shema\PycharmProjects\multimedia processing algorithm\kotik.MP4', cv2.CAP_ANY)

    print_info(cap)

    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        cv2.namedWindow('Kotik c galstukom', cv2.WINDOW_NORMAL)
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # отдельный метод поскольку VideoCapture не содержит методов изменения гаммы
        cv2.resizeWindow('Kotik c galstukom', 640, 480) # изменение размера окна
        cv2.imshow("Kotik c galstukom", new_frame)  # Отображение кадра

        # Ожидание 1 мс и проверка нажатия клавиши 'Esc' (код 27)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()

def show_web_video():
    #захват видео
    cap = cv2.VideoCapture(0)

    print_info(cap) #вывод информации о видео

    #установка новых значений видео
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FPS , 15)

    print_info(cap)

    while True:
        ret, frame = cap.read()  # Чтение текущего кадра
        if not ret:  # Проверка на успешное чтение кадра
            break

        cv2.imshow("Kotik", frame)  # Отображение кадра

        # Ожидание 1 мс и проверка нажатия клавиши 'Esc' (код 27)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()

'''Задание 4 Записать видео из файла в другой файл.'''
def save_video():
    video = cv2.VideoCapture(r'C:\Users\shema\PycharmProjects\multimedia processing algorithm\kotik.MP4', cv2.CAP_ANY)
    ok, img = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) #можно убрать и выбирать количество кадров; если оно больше чем реальное кол-во в видео, то видео будет ускорено

    fourcc = cv2.VideoWriter_fourcc(*'XVID') #это функция, которая задаёт кодек для записи видео.fourcc — это "четырёхсимвольный код", который используется для обозначения формата кодека, применяемого для сжатия видеофайла.
    video_writer = cv2.VideoWriter("save_video_result.avi", fourcc, fps, (w, h))
    while (True):
        ok, img = video.read()
        if not ok:  # Проверка на успешное чтение кадра
            break

        cv2.imshow('The Cat', img)
        video_writer.write(img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()

'''Задание 5 
Прочитать изображение, перевести его в формат HSV.
Вывести на экран два окна, в одном изображение в формате HSV, в другом –
исходное изображение.'''
def rgb_to_hsv():
    img = cv2.imread('ferrari.jpg', 1)
    cv2.namedWindow('RGB', cv2.WINDOW_NORMAL)
    cv2.imshow('RGB', img)

    cv2.namedWindow('HSV', cv2.WINDOW_NORMAL)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV', hsv_img)

    cv2.waitKey(0)

'''Задание 6 (самостоятельно)
Прочитать изображение с камеры. Вывести в центре на экране Красный крест в формате, как на изображении.
Указать команды, которые позволяют это сделать.'''
def red_cross():
    cap = cv2.VideoCapture(0)

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    rectangles = np.array([  # значения [x1, y1], [x2, y2]
        [[0, 140], [260, 180]],  # Горизонтальная полоса креста
        [[110, 0], [150, 140]],  # Верхняя вертикальная часть
        [[110, 180], [150, 320]]  # Нижняя вертикальная часть
    ])

    #rectangles = np.int32(rectangles * 2)  # увеличить или уменьшить крест
    offset_x = frame_w // 2 - rectangles[:, :, 0].max() // 2
    offset_y = frame_h // 2 - rectangles[:, :, 1].max() // 2

    while True:
        ret, frame = cap.read()
        if not ret or cv2.waitKey(1) & 0xFF == 27:
            break

        #размытие горизонтальной линии
        x1, y1 = rectangles[0][0]
        x2, y2 = rectangles[0][1]
        mask = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)
        mask = cv2.rectangle(mask, (x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), (255, 255, 255), -1)
        #blur = cv2.stackBlur(frame, (63, 63))
        blur = cv2.GaussianBlur(frame, (63, 63), 0)
        frame[mask == 255] = blur[mask == 255]

        for rect in rectangles:
            x1, y1 = rect[0]
            x2, y2 = rect[1]
            cv2.rectangle(frame, (x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), (0, 0, 255), 2)

        cv2.imshow("Red cross", frame)

    cap.release()
    cv2.destroyAllWindows()

'''Задание 7 (самостоятельно) 
Отобразить информацию с вебкамеры,
записать видео в файл, продемонстрировать видео.'''
def save_web_video():
    video = cv2.VideoCapture(0, cv2.CAP_ANY)
    ok, img = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) #можно убрать и выбирать количество кадров; если оно больше чем реальное кол-во в видео, то видео будет ускорено

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("save_web_video_result.avi", fourcc, fps, (w, h))
    while (True):
        ok, img = video.read()
        if not ok:  # Проверка на успешное чтение кадра
            break
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey_img_color = cv2.cvtColor(grey_img, cv2.COLOR_GRAY2BGR)
        '''В это месте может возникать ошибка
        Если переводить видео в черно-белое, то оно становится одноканальным
        Нужно вернуть его в цветной формат (но по факту оно останется черно-белым)'''


        cv2.imshow('The Cat', grey_img)
        video_writer.write(grey_img_color)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()

'''Задание 8 (самостоятельно) Залить крест одним из 3 цветов – красный,
зеленый, синий по следующему правилу: НА ОСНОВАНИИ ФОРМАТА RGB
определить, центральный пиксель ближе к какому из цветов красный,
зеленый, синий и таким цветом заполнить крест.'''
def fill_the_red_cross():
    cap = cv2.VideoCapture(0)

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    rectangles = np.array([  # значения [x1, y1], [x2, y2]
        [[0, 140], [260, 180]],  # Горизонтальная полоса креста
        [[110, 0], [150, 140]],  # Верхняя вертикальная часть
        [[110, 180], [150, 320]]  # Нижняя вертикальная часть
    ])

    # rectangles = np.int32(rectangles * 2)  # увеличить или уменьшить крест
    offset_x = frame_w // 2 - rectangles[:, :, 0].max() // 2
    offset_y = frame_h // 2 - rectangles[:, :, 1].max() // 2

    while True:
        ret, frame = cap.read()
        if not ret or cv2.waitKey(1) & 0xFF == 27:
            break

        # выяснение цвета центрального пикселя
        target = [int(frame.shape[1] / 2), int(frame.shape[0] / 2)]  # Координаты центрального пикселя
        central_pixel_bgr = frame[target[1], target[0]]  # Получение цвета центрального пикселя в BGR

        #r,g,b = int(central_pixel_rgb[0]), int(central_pixel_rgb[1]), int(central_pixel_rgb[2])

        max_color_index = np.argmax(central_pixel_bgr)
        color = [0]*3
        color[max_color_index] = 255

        print(central_pixel_bgr[::-1]) #вывод цвета пикселя в rgb

        nf=np.zeros((frame_h, frame_w, 3), dtype=np.uint8) #пустой фрейм (массив 3х измерений) нужный для того, чтобы держать в себе прямоугольник
        for rect in rectangles:
            x1, y1 = rect[0]
            x2, y2 = rect[1]
            cv2.rectangle(nf, (x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), color, -1)

        result_frame = cv2.addWeighted(frame, 1, nf, 0.5, 0)
        cv2.imshow("Filled red cross", result_frame)

    cap.release()
    cv2.destroyAllWindows()


'''Задание 9 (самостоятельно). Подключите телефон, подключитесь к его
камере, выведете на экран видео с камеры. Продемонстрировать процесс на
ноутбуке преподавателя и своем телефоне.'''
def stream_video_from_phone():
    video = cv2.VideoCapture("http://10.204.152.242:8080/video")
    #video = cv2.VideoCapture(1)

    if not video.isOpened():
        print("Ошибка: Не удалось подключиться к видеопотоку")
        return

    while True:
        ok, img = video.read()

        if not ok:
            print("Ошибка: Не удалось прочитать кадр")
            break

        cv2.namedWindow('PhoneStream', cv2.WINDOW_NORMAL)
        # Отображение кадра
        cv2.imshow('PhoneStream', img)

        # Остановка по нажатию клавиши 'Esc'
        if cv2.waitKey(20) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()

#show_photo() #2
#show_video() #3
#show_web_video() #3
#save_video() #4
#rgb_to_hsv() #5
#red_cross() #6
#save_web_video() #7
#fill_the_red_cross() #8
stream_video_from_phone() #9
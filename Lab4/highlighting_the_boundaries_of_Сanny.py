import cv2
import numpy as np


'''Задание 1 Реализовать метод, который принимает в качестве строки
полный адрес файла изображения, читает изображение, переводит его в черно
белый цвет и выводит его на экран применяет размытие по Гауссу и выводит
полученное изображение на экран.'''

def GaussBlur(img_path,k_size, deviation):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return cv2.GaussianBlur(img, (k_size, k_size), deviation)

'''Задание 2 Модифицировать построенный метод так, чтобы в результате
вычислялось и выводилось на экран две матрицы – матрица значений длин и
матрица значений углов градиентов всех пикселей изображения.'''

def get_angle_number(x, y, tg):
    if (x >= 0 and y <= 0 and tg < -2.414) or (x <= 0 and y <= 0 and tg > 2.414):
        return 0
    elif x >= 0 and y <= 0 and tg < -0.414:
        return 1
    elif (x >= 0 and y <= 0 and tg > -0.414) or (x >= 0 and y >= 0 and tg < 0.414):
        return 2
    elif x >= 0 and y >= 0 and tg < 2.414:
        return 3
    elif (x >= 0 and y >= 0 and tg > 2.414) or (x <= 0 and y >= 0 and tg < -2.414):
        return 4
    elif x <= 0 and y >= 0 and tg < -0.414:
        return 5
    elif (x <= 0 and y >= 0 and tg > -0.414) or (x <= 0 and y <= 0 and tg < 0.414):
        return 6
    elif x <= 0 and y <= 0 and tg < 2.414:
        return 7

def convolution(img, kernel):
    #Операция свертки
    height, width = img.shape[:2]
    k_size = len(kernel)
    processed_image = np.zeros_like(img, np.int32)

    # применяем фильтр к пикселям картинки
    for x in range(k_size // 2, height - k_size // 2):
        for y in range(k_size // 2, width - k_size // 2):
            # свертка
            val = 0
            for k in range(-(k_size // 2), k_size // 2 + 1):
                for l in range(-(k_size // 2), k_size // 2 + 1):
                    val += img[x + k, y + l] * kernel[k + (k_size // 2), l + (k_size // 2)]
            processed_image[x, y] = val

    return processed_image

'''Задание 3 Модифицировать метод так, чтобы он выполнял подавление
немаксимумов и выводил полученное изображение на экран. Рассмотреть
изображение, сделать выводы.'''
def suppression_of_non_maximums(img,Gx,Gy,tg,len_gradient):
    edges = np.zeros_like(img)
    for y in range(1, edges.shape[0] - 1):
        for x in range(1, edges.shape[1] - 1):
            angle = get_angle_number(Gx[y, x], Gy[y, x], tg[y, x])
            if angle == 0 or angle == 4:
                neighbor1 = [y - 1, x]
                neighbor2 = [y + 1, x]
            elif angle == 1 or angle == 5:
                neighbor1 = [y - 1, x + 1]
                neighbor2 = [y + 1, x - 1]
            elif angle == 2 or angle == 6:
                neighbor1 = [y, x + 1]
                neighbor2 = [y, x - 1]
            elif angle == 3 or angle == 7:
                neighbor1 = [y + 1, x + 1]
                neighbor2 = [y - 1, x - 1]
            else:
                raise Exception('Угол не определён')
            if (len_gradient[y, x] >= len_gradient[neighbor1[0], neighbor1[1]] and
                    len_gradient[y, x] > len_gradient[neighbor2[0], neighbor2[1]]):
                edges[y, x] = 255

    return edges



'''Задание 4 Модифицировать метод так, чтобы он выполнял двойную
пороговую фильтрацию и выводил полученное изображение на экран.'''
def double_threshold(img,len_gradient, max_grad_len, low_percent, high_percent):
    print(max_grad_len)
    l_percent = low_percent
    h_percent = high_percent

    low_level = int(max_grad_len * l_percent)
    high_level = int(max_grad_len * h_percent)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x] > 0:
                if len_gradient[y, x] < low_level:
                    img[y, x] = 0
                elif len_gradient[y, x] < high_level:
                    keep = False
                    for neighbor_y in (y - 1, y, y + 1):
                        for neighbor_x in (x - 1, x, x + 1):
                            if neighbor_y != y or neighbor_x != x:
                                if (img[neighbor_y, neighbor_x] > 0 and
                                        len_gradient[neighbor_y, neighbor_x] >= high_level):
                                    keep = True
                    if not keep:
                        img[y, x] = 0


    return img

def Canny_method(kernel_size=5,deviation=0,low_percent=0.02, high_percent=0.4,img_path='ferrari.jpg'):
    blrd_img = GaussBlur(img_path, kernel_size, deviation)
    sobelX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobelY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    #Применение свертки к размытому изображению
    Gx,Gy = convolution(blrd_img, sobelX), convolution(blrd_img, sobelY)


    #Вычисление градиентов и угльов
    len_gradient = np.sqrt(np.add(np.square(Gx), np.square(Gy)))
    max_grad_len = len_gradient.max()
    tg = np.divide(Gy, Gx)
    tg = np.nan_to_num(tg)
    cv2.imshow('gradients', (len_gradient / max_grad_len * 255).astype(np.uint8))

    # Подавление немаксимумов
    img_border = suppression_of_non_maximums(blrd_img,Gx,Gy,tg,len_gradient)
    cv2.imshow('img border no filter ', img_border)

    # Применение двойной пороговой фильтрации
    thresholded_img = double_threshold(img_border,len_gradient,max_grad_len,low_percent,high_percent)
    cv2.imshow('Filtered Image', thresholded_img)
    cv2.waitKey(0)


'''Задание 5 (самостоятельно). Провести опыты для различных параметров
размытия и различных пороговых значений градиента, определить наилучшие
параметры для Вашего изображения. Показать преподавателю значения
параметров и результат работы на следующем занятии.'''
#Сравнение отклонения
Canny_method(5,0.005,0.02,0.4)
Canny_method(5,5,0.02,0.4)

#Сравнение размера ядра
Canny_method(5,0.005,0.02,0.4)
Canny_method(11,0.02,0.4)

#Сравнение двойной фильтрации
Canny_method(5,0.005,0.02,0.4)
Canny_method(5,0.005,0.1,0.6)

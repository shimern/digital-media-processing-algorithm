import cv2
import numpy as np


'''Задание 1 Выполнить пункты 1 и 2 алгоритма, то есть построить
матрицу Гаусса. Просмотреть итоговую матрицу для размерностей 3, 5, 7'''

def build_a_Gaussian_matrix():

    kernel_sizes = [3,5,7] #размер ядра
    deviation = 3 #отклонение
    for k_size in kernel_sizes:
        kernel = np.zeros((k_size,k_size))
        a = b = k_size//2 #математическое ожидание - координаты центрального пикселя ядра
        for i in range(k_size):
            for j in range(k_size):
                kernel[i,j] = gauss_func(deviation,a,b,i,j)

        print("Отклонение: ", deviation)
        print("Размерность: ", k_size)
        print("Ядро: ", kernel)
        print()


#Функция Гаусса
def gauss_func(deviation,a,b,x,y):
        m1 = 1 / (2 * np.pi * (deviation**2))
        m2 = np.exp(-((x - a) ** 2 + (y - b) ** 2) / (2*(deviation**2)))

        return m1 * m2



'''Задание 2 Нормировать полученную матрицу Гаусса. Протестировать
результаты на матрицах из предыдущего пункта.'''
def Normalize_the_resulting_Gaussian_matrix():
    kernel_sizes = [3, 5, 7]  # размер ядра
    deviation = 3  # отклонение
    for k_size in kernel_sizes:
        kernel = np.zeros((k_size, k_size))
        a = b = k_size // 2  # математическое ожидание - координаты центрального пикселя ядра
        for i in range(k_size):
            for j in range(k_size):
                kernel[i, j] = gauss_func(deviation, a, b, i, j)

        print("Отклонение: ", deviation)
        print("Размерность: ", k_size)
        print("Ядро до нормализации: ", kernel)

        # нормализуем для сохранения яркости изображения
        sum = 0
        for i in range(k_size):
            for j in range(k_size):
                sum += kernel[i, j]

        for i in range(k_size):
            for j in range(k_size):
                kernel[i, j] /= sum

        print("Ядро после нормализации: ",kernel)
        print()

'''Задание 3 Реализовать фильтр Гаусса средствами языка python.'''
def GaussBlur(img,k_size,deviation):

    height, width = img.shape[0],img.shape[1]

    kernel = np.zeros((k_size, k_size))
    a = b = k_size // 2  # математическое ожидание - координаты центрального пикселя ядра
    for i in range(k_size):
        for j in range(k_size):
            kernel[i, j] = gauss_func(deviation, a, b, i, j)

    print("Отклонение: ", deviation)
    print("Размерность: ", k_size)
    print("Ядро до нормализации: ", kernel)

    # нормализуем для сохранения яркости изображения
    sum = 0
    for i in range(k_size):
        for j in range(k_size):
            sum += kernel[i, j]

    for i in range(k_size):
        for j in range(k_size):
            kernel[i, j] /= sum

    print("Ядро после нормализации: ",kernel)

    blured_img = img.copy()

    #применяем фильтр к пикселям картинки
    for x in range(k_size//2,height-k_size//2):
        for y in range(k_size//2,width-k_size//2):
            # свертка
            val = 0
            for k in range(-(k_size // 2), k_size // 2 + 1):
                for l in range(-(k_size // 2), k_size // 2 + 1):
                    val += img[x + k, y + l] * kernel[k + (k_size // 2), l + (k_size // 2)]
            blured_img[x, y] = val

    return blured_img


'''Задание 4 Применить данный фильтр для двух разных значений
среднего квадратичного отклонения и двух разных размерностей матрицы
свертки, сравнить результаты для ОДНОГО изображения.'''
def GaussBlurCompareValues():

    img = cv2.imread('ferrari.jpg', 0)
    height, width = img.shape[0],img.shape[1]

    kernel_sizes = [5,7]  # размер ядра
    deviations = [0,30]  # отклонение
    for p in range(2):
        k_size,deviation  = kernel_sizes[p], deviations[p]
        kernel = np.zeros((k_size, k_size))
        a = b = k_size // 2  # математическое ожидание - координаты центрального пикселя ядра
        for i in range(k_size):
            for j in range(k_size):
                kernel[i, j] = gauss_func(deviation, a, b, i, j)

        print("Отклонение: ", deviation)
        print("Размерность: ", k_size)
        print("Ядро до нормализации: ", kernel)

        # нормализуем для сохранения яркости изображения
        sum = 0
        for i in range(k_size):
            for j in range(k_size):
                sum += kernel[i, j]

        for i in range(k_size):
            for j in range(k_size):
                kernel[i, j] /= sum

        print("Ядро после нормализации: ",kernel)

        blured_img = img.copy()

        #применяем фильтр к пикселям картинки
        for x in range(k_size//2,height-k_size//2):
            for y in range(k_size//2,width-k_size//2):
                # свертка
                val = 0
                for k in range(-(k_size // 2), k_size // 2 + 1):
                    for l in range(-(k_size // 2), k_size // 2 + 1):
                        val += img[x + k, y + l] * kernel[k + (k_size // 2), l + (k_size // 2)]
                blured_img[x, y] = val

        cv2.namedWindow('Img', cv2.WINDOW_NORMAL)
        cv2.imshow('Img', img)

        cv2.namedWindow('Blured Img', cv2.WINDOW_NORMAL)
        cv2.imshow('Blured Img', blured_img)
        cv2.waitKey(0)



'''Задание 5 Реализовать размытие Гаусса встроенным методом библиотеки OpenCV, сравнить результаты с Вашей реализацией.'''
def CompareGaussBlur():
    img = cv2.imread('ferrari.jpg', 0)
    blur_lib = cv2.GaussianBlur(img, (5, 5), 1)
    blur_mine = GaussBlur(img,5,1)

    cv2.namedWindow('Img', cv2.WINDOW_NORMAL)
    cv2.imshow('Img', img)

    cv2.namedWindow('Blured Img by me', cv2.WINDOW_NORMAL)
    cv2.imshow('Blured Img by me', blur_mine)

    cv2.namedWindow('Blured Img by lib', cv2.WINDOW_NORMAL)
    cv2.imshow("Blured Img by lib", blur_lib)
    cv2.waitKey(0)


'''Задание 6 (самостоятельно) Реализовать размытие Гаусса средствами
любого другого языка программирования.'''

#build_a_Gaussian_matrix() #1
#Normalize_the_resulting_Gaussian_matrix() #2
#GaussBlur() #3
#GaussBlurCompareValues() #4
CompareGaussBlur() #5

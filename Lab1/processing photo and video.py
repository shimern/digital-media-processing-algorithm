#Задание 1 Установить библиотеку OpenCV.
import cv2

'''Задание 2 Вывести на экран изображение. Протестировать три
возможных расширения, три различных флага для создания окна и три
различных флага для чтения изображения.'''

cv2.namedWindow('Display window',cv2.WINDOW_AUTOSIZE) #размер подгоняется под фотку
img = cv2.imread('ferrari.jpg', 0) #Загружает изображение в градациях серого (черно-белое).
cv2.imshow('Display window',img)
cv2.waitKey(0)

cv2.namedWindow('Display window',cv2.WINDOW_NORMAL) #Позволяет изменять размер окна вручную, фото растягивается
img = cv2.imread('ferrari.jpg', -1) #Загружает изображение с сохранением всех каналов, включая альфа-канал, если он есть.
cv2.imshow('Display window',img)
cv2.waitKey(0)

cv2.namedWindow('Display window',cv2.WINDOW_KEEPRATIO) #Сохраняет исходное соотношение сторон изображения при изменении размера окна
img = cv2.imread('ferrari.jpg', 1) # Загружает цветное изображение по умолчанию. При этом все цветные каналы (BGR) сохраняются, но альфа-канал (прозрачность) игнорируется.
cv2.imshow('Display window',img)
cv2.waitKey(0)

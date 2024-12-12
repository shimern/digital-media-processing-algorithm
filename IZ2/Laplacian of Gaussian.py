import cv2
import numpy as np

# Загружаем изображение в градациях серого
image = cv2.imread('images/img6.jpg', cv2.IMREAD_GRAYSCALE)

# Шаг 1: Сглаживание с помощью гауссианова фильтра
sigma = 1.0
blurred = cv2.GaussianBlur(image, (5, 5), sigma)

# Шаг 2: Применение лапласиана (LoG)
laplacian = cv2.Laplacian(blurred, cv2.CV_64F)

# Шаг 3: Нахождение пересечений нуля
zero_crossing = np.zeros_like(laplacian, dtype=np.uint8)
rows, cols = laplacian.shape
for i in range(1, rows - 1):
    for j in range(1, cols - 1):
        # Проверяем смену знака у соседних пикселей
        patch = laplacian[i-1:i+2, j-1:j+2]
        if (np.max(patch) > 0 and np.min(patch) < 0):
            zero_crossing[i, j] = 255  # Это граница

# Шаг 4: Вычисление амплитуды (модуля значений LoG)
amplitude = np.abs(laplacian)

# Автоматический расчет порогов
max_amplitude = np.max(amplitude)  # Максимальное значение амплитуды
lower_threshold = 0.1 * max_amplitude  # Нижний порог (10% от максимума)
upper_threshold = 0.5 * max_amplitude  # Верхний порог (50% от максимума)

# Вывод порогов для проверки
print(f"Lower threshold: {lower_threshold}")
print(f"Upper threshold: {upper_threshold}")

# Шаг 5: Пороговая фильтрация
edges = np.zeros_like(amplitude, dtype=np.uint8)
strong_edges = (amplitude > upper_threshold)
weak_edges = (amplitude > lower_threshold) & (amplitude <= upper_threshold)

# Учитываем только сильные границы и слабые, связанные с ними
edges[strong_edges] = 255
edges[weak_edges] = 128  # Опционально, для визуализации слабых границ

# Сохраняем результат
cv2.imshow('edges.jpg', edges)
cv2.waitKey(0)
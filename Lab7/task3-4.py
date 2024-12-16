import csv
import pathlib
import cv2
import re
import pytesseract
from pytesseract import Output
from difflib import SequenceMatcher
import statistics

# Указываем путь к исполняемому файлу Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Функция для получения абсолютного пути относительно местоположения текущего скрипта
def rel_path(rel_path):
    # Вычисляем абсолютный путь на основе текущего расположения файла
    path = pathlib.Path(__file__).parent / rel_path
    return path

# Функция для очистки строки от лишних символов
def clear_str(str):
    # Преобразуем строку к нижнему регистру
    str = str.lower()
    # Удаляем ненужные символы, включая цифры и пунктуацию
    str = re.sub(
        r"[0123456789\!\#\$\%\^\&\*\(\)\_\~@\`\n\/\|\,\"\<\°\„\?\.\«\’\‚\”\“\®\¥\>\`\'\—\™\‘\:\ \]\[\{\}\=\+\-\\]",
        " ",
        str,
    )
    return str

# Основная функция для тестирования распознавания текста
def test_recognition(rec_type, val_type, dataset_name, show_img=False):
    output_str = ""  # Строка для записи результатов
    labels = {}  # Словарь для хранения меток (истинного текста для изображений)
    images_count = 0  # Счетчик обработанных изображений
    correct_guesses = 0  # Счетчик правильных угадываний (для binary_correct)
    similarities = []  # Список для хранения коэффициентов схожести (для similarity)
    dict_for_avg_of_aug_dataset = {}  # Для усреднённого результата из аугментированных данных

    # Читаем метки из файла labels.csv
    with open(
        str(rel_path(dataset_name + "/labels.csv")), newline="", encoding="utf-8"
    ) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="'")
        for row in reader:
            labels[row[0]] = row[1]  # Записываем имя файла и соответствующую метку

    # Получаем список всех файлов изображений в директории датасета
    img_files = list(
        pathlib.Path(str(rel_path(dataset_name + "/"))).glob("*.jpg")
    )

    # Обрабатываем каждое изображение из списка
    for img_file in img_files:
        # Загружаем изображение в градациях серого
        img = cv2.imread(str(img_file.resolve()), 0)
        # Получаем истинное значение текста для текущего изображения
        groud_truth = labels[img_file.name]

        # Распознавание текста в зависимости от типа rec_type
        if rec_type == "straight_recognition":
            # Простое распознавание текста с помощью Tesseract
            result = pytesseract.image_to_string(img, lang="rus+eng")
        elif rec_type == "boxes_recognition":
            # Распознавание текста посимвольно с координатами букв
            h, w = img.shape
            boxes = pytesseract.image_to_boxes(img, lang="rus+eng")

            # Визуализация ограничивающих рамок вокруг символов
            for box in boxes.splitlines():
                box_data = box.split(" ")
                cv2.rectangle(
                    img,
                    (int(box_data[1]), h - int(box_data[2])),
                    (int(box_data[3]), h - int(box_data[4])),
                    (0, 255, 0),
                    2,
                )
            # Формируем строку из распознанных символов
            result = "".join([sym_data.split(" ")[0] for sym_data in boxes.split("\n")])
        elif rec_type == "filtered_recognition":
            # Распознавание текста с предварительной очисткой строк
            result = pytesseract.image_to_string(img, lang="rus+eng")
            groud_truth = clear_str(groud_truth)
            result = clear_str(result)
        elif rec_type == "avg_of_aug":
            # Распознавание для аугментированных данных, собираем результаты
            result = pytesseract.image_to_string(img, lang="rus+eng")
            img_name_wo_aug = img_file.name.split("_")[0]  # Убираем постфикс аугментации
            if img_name_wo_aug in dict_for_avg_of_aug_dataset:
                dict_for_avg_of_aug_dataset[img_name_wo_aug].append(result)
            else:
                dict_for_avg_of_aug_dataset[img_name_wo_aug] = [result]

        # Удаляем символы новой строки из результата
        result = "".join(result.splitlines())

        # Записываем результат в строку вывода
        output_str += f"{img_file.name} | {groud_truth} | {result}\n"

        # Оценка результата в зависимости от типа val_type
        if val_type == "binary_correct":
            # Проверяем, содержит ли результат истинный текст или наоборот
            if (
                result.lower() in groud_truth.lower()
                or groud_truth.lower() in result.lower()
            ):
                correct_guesses += 1
        elif val_type == "similarity":
            # Расчет коэффициента схожести между строками
            similarity = SequenceMatcher(
                None, groud_truth.lower(), result.lower()
            ).ratio()
            similarities.append(similarity)

        images_count += 1  # Увеличиваем счетчик изображений

        # Печатаем распознанный текст в консоль
        print(result)
        # Показываем изображение, если включен флаг show_img
        if show_img:
            cv2.imshow("captcha", img)
            cv2.waitKey()

    output_str += "\n"

    # Для обработки результатов аугментации
    if rec_type == "avg_of_aug":
        images_count = 0
        similarities = []
        correct_guesses = 0

        for key in dict_for_avg_of_aug_dataset.keys():
            results = dict_for_avg_of_aug_dataset[key]

            if val_type == "binary_correct":
                for result in results:
                    if (
                        result.lower() in groud_truth.lower()
                        or groud_truth.lower() in result.lower()
                    ):
                        correct_guesses += 1
                        break
            elif val_type == "similarity":
                max_similarity = 0
                for result in results:
                    similarity = SequenceMatcher(
                        None, groud_truth.lower(), result.lower()
                    ).ratio()
                    max_similarity = max(similarity, max_similarity)
                similarities.append(max_similarity)

            images_count += 1

    # Подсчет и запись итоговой статистики
    if val_type == "binary_correct":
        output_str += f"Угадано {correct_guesses} / {images_count} капч"
    elif val_type == "similarity":
        output_str += (
            f"Средняя схожесть: {statistics.fmean(similarities) * 100}%"
        )

    # Сохранение результатов в файл
    with open(
        str(
            rel_path(
                "results_" + val_type + "_" + rec_type + "_" + dataset_name + ".txt"
            )
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(output_str)

# Главная функция для запуска тестов
def main():
    # Тестирование усреднённых результатов из аугментированного набора данных
    test_recognition("avg_of_aug", "binary_correct", "dataset2", show_img=False)
    test_recognition("avg_of_aug", "similarity", "dataset2", show_img=False)

    # Тестирование с предварительной фильтрацией текста
    test_recognition(
        "filtered_recognition", "binary_correct", "dataset2", show_img=False
    )
    test_recognition("filtered_recognition", "similarity", "dataset", show_img=False)
    test_recognition("filtered_recognition", "similarity", "dataset2", show_img=False)
    test_recognition(
        "filtered_recognition", "binary_correct", "dataset", show_img=False)

import cv2
import numpy as np


def detect_angles(image):
    # Загрузка изображения
    image_bytes = np.asarray(bytearray(image.read()),
                             dtype=np.uint8)
    # Декодируем байтовый массив в изображение OpenCV
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Улучшение контраста с использованием CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    # Применение гауссова размытия
    blurred = cv2.GaussianBlur(enhanced_gray, (5, 5), 0)

    # Применение адаптивного порогового значения
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 55, 2)

    # Усиленная морфологическая обработка для улучшения контуров
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh,
                             cv2.MORPH_CLOSE, kernel,
                             iterations=2)
    morph = cv2.erode(morph, kernel, iterations=1)
    morph = cv2.dilate(morph, kernel, iterations=1)

    # Применение метода Canny для обнаружения границ
    edged = cv2.Canny(morph, 50, 150)

    # Применение функции HoughLinesP для обнаружения линий
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 50,
                            minLineLength=25, maxLineGap=25)

    # Создание изображения для отрисовки линий
    line_image = np.copy(image)

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image,
                         (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Поиск контуров после объединения линий
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Фильтрация контуров по площади и форме
    rectangles = []
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Игнорирование маленьких контуров
            # Аппроксимируем контур многоугольником
            epsilon = 0.1 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # Проверяем, что контур имеет форму прямоугольника (4 вершины) и углы близки к прямым
            if len(approx) == 4:
                angles = []
                for i in range(4):
                    p1 = approx[i][0]
                    p2 = approx[(i + 1) % 4][0]
                    p3 = approx[(i + 2) % 4][0]
                    v1 = [p1[0] - p2[0], p1[1] - p2[1]]
                    v2 = [p3[0] - p2[0], p3[1] - p2[1]]
                    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                    angles.append(np.degrees(angle))

                if all(80 <= angle <= 100 for angle in angles):  # Проверка на прямые углы
                    rectangles.append(approx)

    # Формирование JSON строки
    points = []
    for rect in rectangles:
        for corner in rect:
            points.append({"x": int(corner[0][0]),
                           "y": int(corner[0][1])})

    return {"points": points}

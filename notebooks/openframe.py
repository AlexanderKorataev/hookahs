import cv2
import matplotlib.pyplot as plt

# Путь к вашему видео
video_path = 'crop7.avi'

# Открыть видео с помощью OpenCV
cap = cv2.VideoCapture(video_path)

# Проверить, успешно ли открылось видео
if not cap.isOpened():
    print("Ошибка: Не удалось открыть видео")
    exit()

# Прочитать первый кадр
ret, frame = cap.read()

# Проверить, успешно ли прочитался кадр
if not ret:
    print("Ошибка: Не удалось прочитать кадр")
    exit()

# Переключить цветовые каналы из BGR в RGB (так Matplotlib ожидает изображения)
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Отображение кадра с помощью Matplotlib
plt.imshow(frame_rgb)
plt.axis('off')
plt.show()

# Освободить ресурсы, связанные с видео
cap.release()

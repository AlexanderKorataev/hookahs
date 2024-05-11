#!/bin/bash

# Путь к видеофайлу
VIDEO_FILE="combined_video.mp4"

# Количество скриншотов
NUM_FRAMES=200

# Создаем папку для кадров, если она не существует
mkdir -p frames

# Получаем длительность видео
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE")

# Вычисляем интервал между кадрами
INTERVAL=$(echo "$DURATION / $NUM_FRAMES" | bc)

# Нарезаем видео на скриншоты
ffmpeg -i "$VIDEO_FILE" -vf "fps=1/$INTERVAL" frames/frame_%03d.jpg -hide_banner

# Переименовываем скриншоты и добавляем им порядковые номера
cd frames || exit
for i in $(seq -f "%03g" 1 "$NUM_FRAMES"); do
    mv "frame_$i.jpg" "frame_$i.jpg"
done

echo "Готово!"


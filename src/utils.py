def crop_image(image, detections: dict, tracker_id: int, padding: int = -2):
    """
    Функция для вырезки скриншотов голов

    Args:
        image: Кадр с которого будут обрезаться головы
        detections: Данные об обноружениях
        tracker_id: Плавающий id пользователя, который ему присваивает трекер
        padding: Внутренние отступы. По дефолту -2.

    Returns:
        Обрезанное изображение
    """

    # Проверка наличия объектов с указанным tracker_id
    if len(detections.xyxy) == 0 or len(detections.tracker_id) == 0:
        print(f"No objects found for tracker_id {tracker_id}")
        return None

    # Получение координат объекта по tracker_id
    mask = (detections.tracker_id == tracker_id)
    if not mask.any():
        print(f"No objects found for tracker_id {tracker_id}")
        return None

    box_coordinates = detections.xyxy[mask][0]
    x1, y1, x2, y2 = box_coordinates

    # Добавление отступа
    x1 -= padding
    y1 -= padding
    x2 += padding
    y2 += padding

    # Проверка границ
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(image.shape[1], int(x2))
    y2 = min(image.shape[0], int(y2))

    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # Проверка размеров
    if x1 >= x2 or y1 >= y2:
        print("Invalid coordinates, unable to crop.")
        return None

    # Обрезка изображения
    object_roi = image[y1:y2, x1:x2]

    return object_roi


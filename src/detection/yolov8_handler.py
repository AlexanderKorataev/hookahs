from ultralytics import YOLO
import supervision as sv

from src.settings import YOLO_MODEL_NAME, CONF_THRESHOLD, TRACKER, SOURCE


import cv2


class YOLOv8Handler:
    def __init__(self, model_path: str = YOLO_MODEL_NAME) -> None:
        """
        Инициализация модели YOLOv8.

        Args:
            model_path (str): Путь к модели YOLOv8.
        """
        self.model = YOLO(model_path)
        # self.model.fuse()


    def process_video(self):
        for result in self.model.track(source=SOURCE, device='cpu', stream=True, verbose=False, conf=float(CONF_THRESHOLD),
                                       tracker=TRACKER, save=True):

            frame = result.orig_img.copy()

            detections = sv.Detections.from_ultralytics(result)

            if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

            detections = detections[(detections.class_id != 60) & (detections.class_id != 1)]
            yield detections, frame
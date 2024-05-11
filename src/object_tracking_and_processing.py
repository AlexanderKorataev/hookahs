from collections import deque
import threading
from datetime import datetime

import numpy as np

from src.detection.yolov8_handler import YOLOv8Handler
from src.utils import crop_image
# from src.restoration_faces.inference_gfpgan import process_image
# from src.face_embedding.face_embedding import FaceEmbedding
from src.object_management.object import Object
# from src.qdrant.vector_manager import VectorManager
from src.send_data.send_data import DataSender
from src.settings import FRAMES_WITHOUT_AN_OBJECT


from typing import Dict, Iterable, List, Set, Tuple

import cv2
from tqdm import tqdm

import supervision as sv



COLORS = sv.ColorPalette.from_hex(["#E6194B", "#3CB44B", "#FFE119", "#3C76D1"])

ZONE_IN_POLYGONS = [
    np.array([[666, 608], [659, 385], [1340, 385], [1362, 542]]),
]

# ZONE_OUT_POLYGONS = [
#     # np.array([[666, 608], [659, 473], [1340, 449], [1362, 542]]),
#     np.array([[666, 608], [659, 385], [1340, 395], [1362, 542]]),
# ]



# class DetectionsManager:
#     def __init__(self) -> None:
#         self.tracker_id_to_zone_id: Dict[int, int] = {}
#         self.counts: Dict[int, Dict[int, Set[int]]] = {}

#     def update(
#         self,
#         detections_all: sv.Detections,
#         detections_in_zones: List[sv.Detections],
#     ) -> sv.Detections:
#         # for zone_in_id, detections_in_zone in enumerate(detections_in_zones):
#         #     for tracker_id in detections_in_zone.tracker_id:
#         #         self.tracker_id_to_zone_id.setdefault(tracker_id, zone_in_id)

#         # print(detections_in_zones)

#         for zone_out_id, detections_in_zone in enumerate(detections_in_zones):
#             for tracker_id in detections_in_zone.tracker_id:
#                 if tracker_id in self.tracker_id_to_zone_id:
#                     zone_in_id = self.tracker_id_to_zone_id[tracker_id]
#                     self.counts.setdefault(zone_out_id, {})
#                     self.counts[zone_out_id].setdefault(zone_in_id, set())
#                     self.counts[zone_out_id][zone_in_id].add(tracker_id)

#                     print(self.counts)

#         # if len(detections_all) > 0:
#         #     detections_all.class_id = np.vectorize(
#         #         lambda x: self.tracker_id_to_zone_id.get(x, -1)
#         #     )(detections_all.tracker_id)
#         # else:
#         #     detections_all.class_id = np.array([], dtype=int)
#         # return detections_all[detections_all.class_id != -1]




def initiate_polygon_zones(
    polygons: List[np.ndarray],
    frame_resolution_wh: Tuple[int, int],
    triggering_anchors: Iterable[sv.Position] = [sv.Position.CENTER],
) -> List[sv.PolygonZone]:
    return [
        sv.PolygonZone(
            polygon=polygon,
            frame_resolution_wh=frame_resolution_wh,
            triggering_anchors=triggering_anchors,
        )
        for polygon in polygons
    ]






# class VideoProcessor:
#     def __init__(
#         self,
#         source_video_path: str,
#         target_video_path: str = None,
#         confidence_threshold: float = 0.65,
#         iou_threshold: float = 0.45,
#     ) -> None:
#         self.conf_threshold = confidence_threshold
#         self.iou_threshold = iou_threshold
#         self.source_video_path = source_video_path
#         self.target_video_path = target_video_path

#         self.tracker = sv.ByteTrack()

#         self.video_info = sv.VideoInfo.from_video_path(source_video_path)
#         self.zones_in = initiate_polygon_zones(
#             ZONE_IN_POLYGONS, self.video_info.resolution_wh, [sv.Position.CENTER]
#         )
#         self.zones_out = initiate_polygon_zones(
#             ZONE_OUT_POLYGONS, self.video_info.resolution_wh, [sv.Position.CENTER]
#         )

#         self.bounding_box_annotator = sv.BoundingBoxAnnotator(color=COLORS)
#         self.label_annotator = sv.LabelAnnotator(
#             color=COLORS, text_color=sv.Color.BLACK
#         )
#         self.trace_annotator = sv.TraceAnnotator(
#             color=COLORS, position=sv.Position.CENTER, trace_length=100, thickness=2
#         )
#         self.detections_manager = DetectionsManager()

#     def process_video(self):
#         frame_generator = sv.get_video_frames_generator(
#             source_path=self.source_video_path
#         )

#         if self.target_video_path:
#             with sv.VideoSink(self.target_video_path, self.video_info) as sink:
#                 for frame in tqdm(frame_generator, total=self.video_info.total_frames):
#                     annotated_frame = self.process_frame(frame)
#                     sink.write_frame(annotated_frame)
#         else:
#             for frame in tqdm(frame_generator, total=self.video_info.total_frames):
#                 annotated_frame = self.process_frame(frame)
#                 if cv2.waitKey(1) & 0xFF == ord("q"):
#                     break
#             cv2.destroyAllWindows()

#     def annotate_frame(
#         self, frame: np.ndarray, detections: sv.Detections
#     ) -> np.ndarray:
        
#         # print(detections)

#         annotated_frame = frame.copy()
#         for i, (zone_in, zone_out) in enumerate(zip(self.zones_in, self.zones_out)):
#             annotated_frame = sv.draw_polygon(
#                 annotated_frame, zone_in.polygon, COLORS.colors[i]
#             )
#             # annotated_frame = sv.draw_polygon(
#             #     annotated_frame, zone_out.polygon, COLORS.colors[i]
#             # )

#         labels = [f"#{tracker_id} {conf:.2f}" for tracker_id, conf in zip(detections.tracker_id, detections.confidence)]

#         # print(detections.tracker_id)
        
#         annotated_frame = self.trace_annotator.annotate(annotated_frame, detections)
#         annotated_frame = self.bounding_box_annotator.annotate(
#             annotated_frame, detections
#         )
#         annotated_frame = self.label_annotator.annotate(
#             annotated_frame, detections, labels
#         )

#         for zone_out_id, zone_out in enumerate(self.zones_out):
#             zone_center = sv.get_polygon_center(polygon=zone_out.polygon)
#             if zone_out_id in self.detections_manager.counts:
#                 counts = self.detections_manager.counts[zone_out_id]
#                 for i, zone_in_id in enumerate(counts):
#                     count = len(self.detections_manager.counts[zone_out_id][zone_in_id])
#                     text_anchor = sv.Point(x=zone_center.x, y=zone_center.y + 40 * i)
#                     annotated_frame = sv.draw_text(
#                         scene=annotated_frame,
#                         text=str(count),
#                         text_anchor=text_anchor,
#                         background_color=COLORS.colors[zone_in_id],
#                     )

#         return annotated_frame

#     def process_frame(self, frame: np.ndarray) -> np.ndarray:
#         results = self.model(
#             frame, verbose=False, conf=self.conf_threshold, iou=self.iou_threshold
#         )[0]

#         detections = sv.Detections.from_ultralytics(results)
#         detections.class_id = np.zeros(len(detections))
#         detections = self.tracker.update_with_detections(detections)



#         detections_in_zones = []
#         detections_out_zones = []

#         for zone_in, zone_out in zip(self.zones_in, self.zones_out):
#             detections_in_zone = detections[zone_in.trigger(detections=detections)]
#             detections_in_zones.append(detections_in_zone)

#         self.detections_manager.update(
#             detections, detections_in_zones
#         )

#         return self.annotate_frame(frame, detections)












class ObjectTrackingAndProcessing:
    def __init__(self) -> None:
        """
        Инициализация объекта для трекинга и обработки видеопотока.
        """
        # self.conf_threshold = confidence_threshold
        # self.iou_threshold = iou_threshold
        # self.source_video_path = source_video_path
        # self.target_video_path = target_video_path

        self.tracker = sv.ByteTrack()

        # self.video_info = sv.VideoInfo.from_video_path(source_video_path)
        self.zones_in = initiate_polygon_zones(
            ZONE_IN_POLYGONS, (1920, 1080), [sv.Position.CENTER]
        )

        # self.zones_out = initiate_polygon_zones(
        #     ZONE_OUT_POLYGONS, (1920, 1080), [sv.Position.CENTER]
        # )

        self.bounding_box_annotator = sv.BoundingBoxAnnotator(color=COLORS)
        self.label_annotator = sv.LabelAnnotator(
            color=COLORS, text_color=sv.Color.BLACK
        )
        self.trace_annotator = sv.TraceAnnotator(
            color=COLORS, position=sv.Position.CENTER, trace_length=100, thickness=2
        )
        # self.detections_manager = DetectionsManager()
        



        self.yolo_handler = YOLOv8Handler()

        self.object_history = {}  # Словарь для хранения истории объектов
        self.frame_count = 0
        self.processed_missing_objects = set()

        self.objects = []

        self.ds = DataSender()


    def process_video_stream(self) -> None:
        """
        Обработка видеопотока и трекинг объектов.
        """
        for detections, frame in self.yolo_handler.process_video():

            detections_in_zones = []

            self.zones_in = initiate_polygon_zones(
            ZONE_IN_POLYGONS, (1920, 1080), [sv.Position.CENTER]
        )

            for zone_in in self.zones_in:
                detections_in_zone = detections[zone_in.trigger(detections=detections)]
                detections_in_zones.append(detections_in_zone)


            # print(detections_in_zones)

            # print("1----------------------------------------------")
            # print(detections)

            # print("2----------------------------------------------")
                
            detections = detections_in_zones[0]



            self.frame_count += 1
            if detections and len(detections.xyxy) > 0:

                for idx in range(len(detections.xyxy)):

                    tracker_id = detections.tracker_id
                    if tracker_id is not None and isinstance(tracker_id, np.ndarray) and len(tracker_id) > idx:

                        tracker_id = int(tracker_id[idx])

                        if tracker_id not in self.object_history:

                            self.object_history[tracker_id] = deque(maxlen=FRAMES_WITHOUT_AN_OBJECT)
                            self.object_history[tracker_id].append(self.frame_count)

                            existing_people = next((p for p in self.objects if p.floating_id == tracker_id), None)
                            if not existing_people:

                                threading.Thread(target=self.handle_new_object, args=(tracker_id, detections, frame)).start() 

                            self.processed_missing_objects.discard(tracker_id)

                        else:
                            
                            self.object_history[tracker_id].append(self.frame_count)

            objects_to_remove = []

            # Итерируемся по истории объектов
            # for tracker_id, frame_numbers in self.object_history.items():

            #     if self.frame_count - frame_numbers[-1] > FRAMES_WITHOUT_AN_OBJECT:
                    

            #         self.handle_missing_object(tracker_id)

            #         objects_to_remove.append(tracker_id)  # Добавляем объект в список для удаления

            # # Удаляем объекты из истории
            # for tracker_id in objects_to_remove:

            #     self.object_history.pop(tracker_id, None)




    def handle_new_object(self, tracker_id: int, detections: dict, frame) -> None: 
        """
        Метод для обработки нового объекта в кадре.

        Args:
            tracker_id (int): id объекта в трекере при отслеживании.
            detections (dict): Обнаружения на кадре.
            frame : Кадр, на котором появился пользователь.
        """

        object_roi = crop_image(frame, detections, tracker_id)

        # if RESTORATION:

        #     img = process_image(object_roi)

        # else:
            
        img = object_roi

        # embedding = FaceEmbedding().generate_embedding(img)[0]

        # vector = embedding['embedding'] # Переименовать!
        # facial_area = embedding['facial_area']


        # user_id_ = self.vm.process_embedding(vector)
        people = Object(user_id=tracker_id, floating_id=tracker_id)
        # people.get_age_or_set(img)

        self.add_passenger(people)
        self.ds.send_data_to_central_server(
            people, 
            # is_inside=True, 
            datetime=datetime.now().isoformat(), 
            image=img
            )

        print(f'Новый объект {people}')

        

# !!!
    # def handle_missing_object(self, tracker_id: int) -> None:
    #     """
    #     Метод для обработки пропавшего объекта из кадра.

    #     Args:
    #         tracker_id (int): id объекта в трекере при отслеживании.
    #     """

    #     found_people = None

    #     for people in self.objects:
    #         if people.floating_id == tracker_id:
    #             found_people = people
    #             break

    #     if found_people:
    #         self.ds.send_data_to_central_server(
    #             found_people, 
    #             is_inside=False,
    #             datetime=datetime.now().isoformat(),
    #             )
    #         self.remove_passenger(found_people)

    #         print(f'Объект пропал из кадра {people}')


    def add_passenger(self, passenger):
        
        self.objects.append(passenger)

    def remove_passenger(self, passenger):

        self.objects.remove(passenger)        
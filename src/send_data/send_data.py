# from dataclasses import asdict
# import json
import requests

# import cv2

# from src.settings import SERVER_URL
# from src.settings import BUS_NUMBER


# class DataSender:
#     def __init__(self) -> None:
#         """
#         Инициализация объекта для отправки данных.
#         """
#         self.central_server_url = SERVER_URL

#     def send_data_to_central_server(self, data, datetime: str, image=None) -> None:
#         # Преобразуйте данные пользователя в JSON-строку

#         # print(data)

#         user_json = json.dumps(asdict(data))
#         user_dict = json.loads(user_json)

#         # print(user_json)

#         # Подготовьте данные для отправки, включая JSON-строку пользователя
#         data_dict = {
#             'id_': user_dict['user_id'],
#             'floating_id': user_dict['floating_id'],
#             'datetime': datetime,

#         }

#         print(data_dict)

#         files = []

#         # Если есть изображение, подготовьте его для отправки
#         if image is not None:
#             image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
#             files.append(('image', ('image.jpg', image_bytes, 'image/jpeg')))
#         else:
#             # Если изображения нет, отправьте пустой файл
#             files.append(('image', ('empty.jpg', b'', 'image/jpeg')))

#         response = requests.post(
#                 f'{self.central_server_url}/api/v1/statistics/data/',
#                 params={
#                     'id_': data_dict['id_'],
#                     'datetime': data_dict['datetime'],
#                     'floating_id': data_dict['floating_id']
#                 },
#                 files=files
#             )

#     def check_internet_connection(self) -> bool:
#         """
#         Метод для проверки корректной отправки данных.

#         Returns:
#             bool : Статаус отправки данных.
#         """
#         try:
#             response = requests.get('http://www.google.com', timeout=5)
#             return True
#         except requests.ConnectionError:
#             return False


import os
import json
from dataclasses import asdict
import cv2

class DataSender:
    def __init__(self, json_file_path: str) -> None:
        """
        Инициализация объекта для отправки данных.

        Args:
            json_file_path (str): Путь к JSON-файлу, куда будут записываться данные.
        """
        self.json_file_path = '1.json'

    def write_data_to_json_file(self, data) -> None:
        """
        Запись данных в JSON-файл.

        Args:
            data (object): Данные, которые будут записаны в JSON-файл.
        """
        with open(self.json_file_path, 'a') as json_file:
            json.dump(asdict(data), json_file)
            json_file.write('\n')

    def send_data_to_central_server(self, data, datetime: str, image=None) -> None:
        """
        Отправка данных на центральный сервер.

        Args:
            data (object): Данные пользователя.
            datetime (str): Временная метка данных.
            image (np.ndarray, optional): Изображение, связанное с данными. По умолчанию None.
        """


        user_json = json.dumps(asdict(data))
        user_dict = json.loads(user_json)

        # print(user_json)

        # Подготовьте данные для отправки, включая JSON-строку пользователя
        data_dict = {
            'id_': user_dict['user_id'],
            'floating_id': user_dict['floating_id'],
            'datetime': datetime,

        }

        self.write_data_to_json_file(data_dict)

    def check_internet_connection(self) -> bool:
        """
        Метод для проверки доступности интернет-соединения.

        Returns:
            bool: True, если интернет-соединение доступно, и False в противном случае.
        """
        try:
            response = requests.get('http://www.google.com', timeout=5)
            return True
        except requests.ConnectionError:
            return False

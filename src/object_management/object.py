from dataclasses import dataclass
from typing import Optional

# from src.age_predict.predict import getAge

@dataclass
class Object:
    user_id: int
    floating_id: int
    # gps_coords: Optional[str] = None
    # age: Optional[int] = None

    # def set_gps_coords(self, gps_coords: str) -> str:
    #     """
    #     Устанавливает GPS-координаты объекту.

    #     Args:
    #         gps_coords (str): GPS-координаты в формате строки.
    #     """
    #     self.gps_coords = gps_coords

    # def get_age_or_set(self, image=None) -> int:
    #     """
    #     Метод, который возвращает возраст объекта. Если возраст не установлен, 
    #     устанавливает его с помощью переданной функции.

    #     Args:
    #         image : Изображение лица.

    #     Returns:
    #         int: Возраст объекта.
    #     """
    #     if self.age is not None:
    #         return self.age
        
    #     self.age = getAge(image)

    #     return self.age
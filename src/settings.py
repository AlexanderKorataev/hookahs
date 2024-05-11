import os


# Идентификатор устройства для доступа к данным
BUS_NUMBER: str                 = str(os.getenv('BUS_NUMBER'))

# Путь к моделе YOLOv8
YOLO_MODEL_NAME: str            = str(os.getenv('YOLO_MODEL_NAME'))
CONF_THRESHOLD: float           = float(os.getenv('CONF_THRESHOLD'))
TRACKER: str                    = str(os.getenv('TRACKER'))

SOURCE: str                     = str(os.getenv('SOURCE'))

# Адрес для отправки данных
SERVER_URL: str                 = str(os.getenv('SERVER_URL'))

# Порог, после которого мы считаем, что люди при сравнении разные
# THRESHOLD: str                  = str(os.getenv('THRESHOLD'))
# COLLECTION_NAME: str            = str(os.getenv('COLLECTION_NAME'))
# QDRANT_LOCATION: str            = str(os.getenv('QDRANT_LOCATION'))

# RESTORATION: bool               = bool(int(os.getenv('RESTORATION')))
FRAMES_WITHOUT_AN_OBJECT: int   = int(os.getenv('FRAMES_WITHOUT_AN_OBJECT'))

import numpy as np
from ultralytics import YOLO

from backend.contants import YOLO_MODEL_NAME


class YOLOWrapper:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL_NAME)

    def predict(self, image_numpy_array: np.array):
        prediction = self.model.predict(image_numpy_array)[0]

        mappings = prediction.names

        classes = [mappings.get(int(val.item())) for val in prediction.boxes.cls]

        if len(classes) == 0:
            return None

        return classes[0]

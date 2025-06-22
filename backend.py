import threading

import cv2
import numpy as np
from ultralytics import YOLO

from contants import YOLO_MODEL_NAME
from controller import Actionable, Act


class YOLOWrapper:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL_NAME)

    def predict(self, image_numpy_array: np.array):
        prediction = self.model.predict(image_numpy_array)[0]

        classes = [int(val.item()) for val in prediction.boxes.cls]

        action = Act.Focus if 0 in classes else Act.Music
        Actionable().start(action)


class CameraHandler:
    def __init__(self, yolo_model):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(3, 200)
        self.vid.set(4, 200)

        self.yolo_model: YOLOWrapper = yolo_model
        self.flag = True

    def start(self):
        memento = 0
        while self.flag:
            rect, frame = self.vid.read()

            if memento % 10 == 0:
                memento = 0
                self.yolo_model.predict(frame)

            # cv2.imshow('Camera', frame)

            memento += 1

            if cv2.waitKey(1) == ord('q'):
                break

    def stop(self):
        self.flag = False

    def __del__(self):
        self.vid.release()
        cv2.destroyAllWindows()


class Backend:
    def __init__(self):
        self.YOLO = YOLOWrapper()
        self.prediction_thread = None
        self.camera = None

    def start(self):
        self.camera = CameraHandler(self.YOLO)
        self.prediction_thread = threading.Thread(target=self.camera.start)
        self.prediction_thread.start()

    def stop(self):
        self.camera.stop()
        self.prediction_thread.join()

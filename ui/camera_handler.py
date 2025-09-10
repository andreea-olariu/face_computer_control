import cv2


class CameraHandler:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(3, 200)
        self.vid.set(4, 200)

    def capture_frame(self):
        return self.vid.read()

    def __del__(self):
        self.vid.release()
        cv2.destroyAllWindows()

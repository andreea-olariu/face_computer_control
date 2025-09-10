import base64

import cv2
import requests

from ui.constants import API


def send_frame_to_api(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    img_base64 = base64.b64encode(buffer).decode("utf-8")
    res = requests.post(f'{API}/image', json={"image": img_base64})

    if res.status_code == 404:
        return "Damn. Nothing detected"

    body = res.json()
    return body.get("predicted")

import base64
import cv2
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from yolo import YOLOWrapper

app = FastAPI()

model = YOLOWrapper()


class ImagePayload(BaseModel):
    image: str


@app.post("/image")
async def post_image(payload: ImagePayload):
    img_bytes = base64.b64decode(payload.image)

    nparr = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = model.predict(img)

    if result is None:
        return JSONResponse(status_code=404, content={"error": "no result"})

    return JSONResponse(status_code=200, content={
        "predicted": result
    })

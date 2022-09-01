import time
import settings
import json
import redis
import torch
import numpy as np
import os

from from_drive import from_onedrive

db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)

weights_path = settings.WEIGHTS_PATH
if not os.path.isfile(weights_path):
    from_onedrive(weights_path)

model = torch.hub.load(
    settings.MODEL_FOLDER,
    "custom",
    path=weights_path,
    source="local",
    force_reload=True,
)
model.conf = 0.2  # NMS confidence threshold
model.agnostic = True
# model.iou  = 0.25  # NMS IoU threshold


def model_inference(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run the ML model to get predictions.
    """

    image_path = os.path.join(settings.UPLOAD_FOLDER, image_name)

    results = model(image_path)

    df_bb = results.xyxy[0].tolist()

    return df_bb


def detection_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get detections and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.
    """

    while True:
        _, msg = db.brpop(settings.REDIS_QUEUE)

        msg = json.loads(msg)

        bb_list = model_inference(msg["image_name"])

        received_msg = {"bouding_boxes": bb_list}

        db.set(msg["id"], json.dumps(received_msg))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    detection_process()

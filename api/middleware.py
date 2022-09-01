import time
import settings
import uuid
import json
import redis

db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)


def model_detect(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from the ML service.
    """

    job_id = str(uuid.uuid4())  # random value
    msg_to_send = {"id": job_id, "image_name": image_name}
    job_data = msg_to_send

    # Send the job to the model service using Redis
    db.rpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop until it received the response from the ML model
    while True:
        # Attempt to get model predictions using job_id
        output = db.get(job_id)

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

        if output == None:
            continue
        else:
            output_dict = json.loads(output)
            db.delete(job_id)
            break
    return output_dict

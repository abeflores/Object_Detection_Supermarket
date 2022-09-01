import os

# Run API in Debug mode
API_DEBUG = True

# It will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# It will store images processed on this folder
PROCESSED_FOLDER = "static/processed/"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

TOKENS = {
    "secret-token-1-abelardo": "Abe",
    "secret-token-2-alfredo": "Alfredo",
    "secret-token-3-federico": "Fede",
    "secret-token-4-jose": "Jose",
    "secret-token-5-gaston": "Gaston",
}

# REDIS settings
# Queue name
REDIS_QUEUE = "api_ml_queue"
# Port
REDIS_PORT = "6379"
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = "redis"
# Sleep parameters which manages the
# interval between requests to the redis queue
API_SLEEP = 0.05

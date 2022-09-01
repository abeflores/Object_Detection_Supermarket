from locust import HttpUser, task, between
from random import choice
import os


class ApiUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def index_page(self):
        self.client.get("/")

    @task(3)
    def detect_endpoint(self):
        """Select a random image from the images folder
        and make a post request with it to /predict endpoint.
        """

        files = os.listdir("images")
        file = choice(files)

        with open(f"images/{file}", "rb") as img:
            file = [("file", (file, img, "image/jpeg"))]
            self.client.post(
                "/detect",
                files=file,
                headers={"Authorization": "Bearer secret-token-5-gaston"},
            )

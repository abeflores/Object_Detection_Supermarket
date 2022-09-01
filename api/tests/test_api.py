import json
from unittest import TestCase
from unittest.mock import patch

from app import app


class TestIntegration(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_predict_bad_parameters(self):
        response = self.client.post(
            "/detect",
            data=json.dumps({"not_a_file": "blabla"}),
            content_type="application/json",
            headers={"Authorization": "Bearer secret-token-5-gaston"},
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data.keys()), 2)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["detections"], None)

    def test_bad_token(self):
        response = self.client.post(
            "/detect",
            data=json.dumps({"not_a_file": "blabla"}),
            content_type="application/json",
            headers={"Authorization": "Bearer secret-token-4-Carlos"},  # Invalid token
        )
        self.assertEqual(response.status_code, 401)

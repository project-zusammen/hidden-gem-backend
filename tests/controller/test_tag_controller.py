import uuid
import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

user_data = {
    "id": 1,
    "public_id": str(uuid.uuid4()),
    "username": "test_user",
    "email": "test_user@gmail.com",
    "password": "test_password",
    "role": "admin",
    "status": "active",
}


tag_data = {
    "name": "This is a test tag.",
}


class TestTagEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.tag_controller.create_tag")
    def test_create_tag(self, mock_create_tag):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": tag_data,
        }
        mock_create_tag.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/tag", json=tag_data, headers=headers)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["name"], res.get("name"))
        mock_create_tag.assert_called_once()

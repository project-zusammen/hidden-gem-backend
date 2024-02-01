import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

user_data = {
    "review_id": "4128525d-7851-4562-839d-ff0479384508",
    "user_id": 1,
}


class TestBookmarkEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.bookmark_controller.create_bookmark")
    def test_create_bookmark(self, mock_create_bookmark):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": user_data,
        }
        token_payload = {
            "id": 1,
            "public_id": "66434932-de79-4800-955a-fa09466c5218",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "role": "user",
            "status": "active",
        }
        token = create_token(token_payload)
        mock_create_bookmark.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/bookmark", json=user_data, headers={"X-API-KEY": token}
            )
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"], res)
        mock_create_bookmark.assert_called_once_with(user_data, token_payload["id"])

    @patch("app.main.controller.bookmark_controller.get_bookmark_by_userid")
    def test_get_bookmark_by_userid(self, mock_get_bookmark_by_userid):
        # ARRANGE
        token_payload = {
            "id": 1,
            "public_id": "66434932-de79-4800-955a-fa09466c5218",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "role": "user",
            "status": "active",
        }
        token = create_token(token_payload)
        expected_response = {
            "status": "success",
            "message": "Successfully get a bookmark.",
            "data": user_data,
        }

        mock_get_bookmark_by_userid.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/bookmark", headers={"X-API-KEY": token})
            result = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["user_id"], user_data["user_id"])
        self.assertEqual(result["review_id"], user_data["review_id"])
        mock_get_bookmark_by_userid.assert_called_once()

    @patch("app.main.controller.bookmark_controller.delete_bookmark")
    def test_delete_bookmark(self, mock_delete_bookmark):
        # ARRANGE
        token_payload = {
            "id": 1,
            "public_id": "66434932-de79-4800-955a-fa09466c5218",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "role": "user",
            "status": "active",
        }
        token = create_token(token_payload)
        expected_response = {
            "status": "success",
            "message": "Successfully deleted.",
        }
        mock_delete_bookmark.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.delete(
                f"/api/bookmark/{token_payload['public_id']}",
                headers={"X-API-KEY": token},
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get("status"), res.get("status"))
        self.assertEqual(expected_response.get("message"), res.get("message"))
        mock_delete_bookmark.assert_called_once()

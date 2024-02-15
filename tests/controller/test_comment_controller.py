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
    "email": "@gmail.com",
    "password": "test_password",
    "role": "admin",
    "status": "active",
}

comment_data_single = {"content": "This is a test comment.", "review_id": "1234ABCD"}

comment_data_multiple = [
    {"content": "This is a test comment 1.", "review_id": "1234ABCD"},
    {"content": "This is a test comment 2.", "review_id": "1234ABCD"},
]

public_id = "public_id_test"


class TestCommentEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.comment_controller.create_comment")
    def test_create_comment(self, mock_create_comment):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": comment_data_single,
        }
        mock_create_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/comment", json=comment_data_single)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["content"], res.get("content"))
        mock_create_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.get_all_comments")
    def test_get_all_comments(self, mock_get_all_comments):
        # ARRANGE
        expected_data = comment_data_multiple
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved comments.",
            "data": expected_data,
        }
        mock_get_all_comments.return_value = expected_response
        page = 1
        count = 2

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/comment?page={page}&count={count}")
            res = json.loads(response.data.decode("utf-8"))
            res = res.get("data")
            first_comment = res[0]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(res, list)
        self.assertEqual(expected_data[0].get("content"), first_comment.get("content"))
        self.assertEqual(
            expected_data[0].get("review_id"), first_comment.get("review_id")
        )
        mock_get_all_comments.assert_called_once()

    @patch("app.main.controller.comment_controller.get_a_comment")
    def test_get_a_comment(self, mock_get_a_comment):
        # ARRANGE
        expected_data = comment_data_single
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved comment.",
            "data": expected_data,
        }

        mock_get_a_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/comment/{public_id}")
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        mock_get_a_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.delete_comment")
    def test_delete_comment(self, mock_delete_comment):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": comment_data_single,
        }

        mock_delete_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.delete(f"/api/comment/{public_id}")
            res = response.get_json()

        # ARRANGE
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        self.assertEqual(
            expected_response["data"].get("review_id"), res["data"].get("review_id")
        )
        mock_delete_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.update_comment")
    def test_update_comment(self, mock_update_comment):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Comment updated successfully.",
            "data": comment_data_single,
        }

        mock_update_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/comment/{public_id}", json=comment_data_single)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        self.assertEqual(
            expected_response["data"].get("review_id"), res["data"].get("review_id")
        )
        mock_update_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.upvote_comment")
    def test_upvote_comment(self, mock_upvote_comment):
        # ARRANGE
        comment_data_single["upvotes"] = 1
        comment_data_single["downvotes"] = 1
        expected_response = {
            "status": "success",
            "message": "Comment upvoted successfully.",
            "data": comment_data_single,
        }

        mock_upvote_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(
                f"/api/comment/{public_id}/vote", json=comment_data_single
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("upvotes"), res["data"].get("upvotes")
        )
        self.assertEqual(
            expected_response["data"].get("downvotes"), res["data"].get("downvotes")
        )
        mock_upvote_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.update_visibility")
    def test_update_visibility(self, mock_update_visibility):
        # ARRANGE
        comment_data_single["visible"] = False
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": comment_data_single,
        }

        mock_update_visibility.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.put(
                f"/api/comment/{public_id}/status",
                json=comment_data_single,
                headers=headers,
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("visible"), res["data"].get("visible")
        )
        mock_update_visibility.assert_called_once()

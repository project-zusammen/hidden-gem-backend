import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app

comment_data = {
    "content": "This is a test comment.",
    "review_id": "1234ABCD"
}

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
            "data": comment_data,
        }
        mock_create_comment.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/comment", json=comment_data)
            result = response.get_json()
            result = result.get("data")
        
        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["content"], result.get("content"))
        mock_create_comment.assert_called_once()

    @patch("app.main.controller.comment_controller.get_all_comments")
    def test_get_all_comments(self, mock_get_all_comments):
        # ARRANGE
        expected_data = [{
            "public_id": "2e6d43d8-9b1f-4dfc-8576-08deb8bcba15",
            "content": "This is a test comment kali ya?",
            "created_at": "2024-01-18T16:06:35",
            "updated_at": "2024-01-18T16:29:03",
            "upvotes": 0,
            "downvotes": 0,
            "visible": True
            }
        ]
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved comments.",
            "data": expected_data,
        }
        mock_get_all_comments.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/comment")
            result = json.loads(response.data.decode("utf-8"))
            result = result.get("data")
            first_comment = result[0]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(expected_data[0].get("content"), first_comment.get("content"))
        mock_get_all_comments.assert_called_once()


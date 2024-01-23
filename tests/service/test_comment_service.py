import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.comment_service import (
    get_all_comments,
    get_a_comment,
    create_comment
)

def generate_fake_public_id():
    return str(uuid.uuid4())

comment_1 = {"public_id": generate_fake_public_id(), "content": "Comment 1", "review_id": "review_id 1"} 
comment_2 = {"public_id": generate_fake_public_id(), "content": "Comment 2", "review_id": "review_id 2"}

class TestReviewService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.comment.Comment.get_all_comments")
    def test_get_all_comments(self, mock_get_all_comments):
        # ARRANGE
        data = [comment_1, comment_2]
        mock_get_all_comments.return_value = data

        # ACT
        response, status_code = get_all_comments()
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully retrieved comments.")
        self.assertEqual(len(result), len(data))

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["content"], data[i]["content"])
            self.assertEqual(result[i]["review_id"], data[i]["review_id"])

        mock_get_all_comments.assert_called_once()

    @patch("app.main.model.comment.Comment.get_comment_by_id")
    def test_get_a_comment(self, mock_get_comment_by_id):
        # ARRANGE
        data = comment_1
        mock_get_comment_by_id.return_value = data

        # ACT
        response, status_code = get_a_comment(public_id = generate_fake_public_id())
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a comment.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["content"], data["content"])
        self.assertEqual(result["review_id"], data["review_id"])

        mock_get_comment_by_id.assert_called_once()

    @patch("app.main.model.comment.Comment.create_comment")
    def test_create_comment(self, mock_create_comment):
        # ARRANGE
        data = comment_1
        mock_create_comment.return_value = data

        # ACT
        response, status_code = create_comment(data)
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["content"], data["content"])
        self.assertEqual(result["review_id"], data["review_id"])

        mock_create_comment.assert_called_once()
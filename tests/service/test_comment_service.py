import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.comment_service import (
    get_all_comments
)

def generate_fake_public_id():
    return str(uuid.uuid4())

class TestReviewService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @oatch("app.main.model.comment.Comment.get_all_comments")
    def test_get_all_comments(self, mock_get_all_comments):
        # Arrange
        comment_1 = {"public_id": generate_fake_public_id(), "content": "Comment 1"}
        comment_2 = {"public_id": generate_fake_public_id(), "content": "Comment 2"}
        mock_get_all_comments.return_value = [comment_1, comment_2]
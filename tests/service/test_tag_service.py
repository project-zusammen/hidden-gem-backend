import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.tag_service import (
    create_tag,
)


def generate_fake_public_id():
    return str(uuid.uuid4())


class TestTagService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.tag.Tag.create_tag")
    def test_create_tag(self, mock_create_tag):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "name": "new tag",
        }
        mock_create_tag.return_value = data

        # Act
        response, status_code = create_tag(data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["name"], data["name"])


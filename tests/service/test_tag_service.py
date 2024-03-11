import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.tag_service import (
    create_tag,
    get_all_tags,
)

tag_data = {
    "name": "new tag",
}


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
    
        mock_create_tag.return_value = tag_data

        # Act
        response, status_code = create_tag(tag_data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["name"], tag_data["name"])
    
    @patch("app.main.model.tag.Tag.get_all_tags")
    def test_get_all_tags(self, mock_get_all_tags):
        # Arrange
        data = [tag_data]
        mock_get_all_tags.return_value = data

        # Act
        response, status_code = get_all_tags()
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result[0]["name"], data[0]["name"])



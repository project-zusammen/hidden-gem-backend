import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.category_service import create_category, get_all_categories


category_data = {
    "name": "food",
}

class TestCategoryService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.category.Category.create_category")
    def test_create_category(self, mock_create_category):
        # Arrange
        data = {
            "public_id": str(uuid.uuid4()),
            "name": "food",
        }
        mock_create_category.return_value = data

        # Act
        response, status_code = create_category(category_data["name"])
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["name"], data["name"])
    
    @patch("app.main.model.category.Category.get_categories")
    def test_get_all_categories(self, mock_get_categories):
        # Arrange
        data = {
            "public_id": str(uuid.uuid4()),
            "name": "food",
        }
        mock_get_categories.return_value = [data]

        # Act
        response, status_code = get_all_categories()
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get.")
        self.assertEqual(result, [data])
        mock_get_categories.assert_called_once()

import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app

category_data = {
    "public_id": str(uuid.uuid4()),
    "name": "food",
}

class TestCategoryEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.category_controller.create_category")
    def test_create_category(self, mock_create_category):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": category_data,
        }
        mock_create_category.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/category", json=category_data)
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"], res)
        mock_create_category.assert_called_once_with(category_data['name'])
    
    @patch("app.main.controller.category_controller.get_all_categories")
    def test_get_all_categories(self, mock_get_all_categories):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully get.",
            "data": [category_data],
        }
        mock_get_all_categories.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/category")
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"], res)
        mock_get_all_categories.assert_called_once()

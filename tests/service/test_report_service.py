import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.report_service import create_report


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

    @patch("app.main.model.report.Report.create_report")
    def test_create_report(self, mock_create_report):
        # Arrange
        public_id = generate_fake_public_id()
        item_id = generate_fake_public_id()
        user_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "type": "review",
            "item_id": item_id,
            "reason": "Test Reason",
            "user_id": user_id,
        }
        mock_create_report.return_value = data

        # Act
        response, status_code = create_report(data, 2)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["type"], data["type"])
        self.assertEqual(result["item_id"], data["item_id"])
        self.assertEqual(result["reason"], data["reason"])

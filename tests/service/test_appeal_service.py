import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.appeal_service import create_appeal


def generate_fake_public_id():
    return str(uuid.uuid4())


appeal_1 = {
    "public_id": generate_fake_public_id(),
    "reason": "Appeal 1",
    "report_id": "report_id 1",
}
appeal_2 = {
    "public_id": generate_fake_public_id(),
    "reason": "Appeal 2",
    "report_id": "report_id 2",
}


class TestAppealService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.appeal.Appeal.create_appeal")
    def test_create_appeal(self, mock_create_appeal):
        # ARRANGE
        data = appeal_1
        mock_create_appeal.return_value = data

        # ACT
        response, status_code = create_appeal(data)
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["report_id"], data["report_id"])

        mock_create_appeal.assert_called_once()

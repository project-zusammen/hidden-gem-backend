import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app

appeal_data = {
    "reason": "This is a test appeal.",
    "report_id": "report_id",
}


class TestAppealEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.appeal_controller.create_appeal")
    def test_create_appeal(self, mock_create_appeal):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": appeal_data,
        }
        mock_create_appeal.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/appeal", json=appeal_data)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["reason"], res.get("reason"))
        mock_create_appeal.assert_called_once()

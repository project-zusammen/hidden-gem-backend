import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app

report_data = {
    "type": "review",
    "item_id": str(uuid.uuid4()),
    "reason": "Test Reason",
}


class TestReportEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.report_controller.create_report")
    def test_create_report(self, mock_create_report):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": report_data,
        }
        mock_create_report.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/report", json=report_data)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["type"], res.get("type"))
        self.assertEqual(expected_response["data"]["item_id"], res.get("item_id"))
        self.assertEqual(expected_response["data"]["reason"], res.get("reason"))
        mock_create_report.assert_called_once()
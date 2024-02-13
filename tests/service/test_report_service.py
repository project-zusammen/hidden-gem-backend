import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.report_service import (
    create_report,
    get_all_reports,
    get_a_report,
    update_report,
)


def generate_fake_public_id():
    return str(uuid.uuid4())


report_data_1 = {
    "public_id": generate_fake_public_id(),
    "user_id": generate_fake_public_id(),
    "type": "review",
    "item_id": generate_fake_public_id(),
    "reason": "Test Reason 1",
}

report_data_2 = {
    "public_id": generate_fake_public_id(),
    "user_id": generate_fake_public_id(),
    "type": "review",
    "item_id": generate_fake_public_id(),
    "reason": "Test Reason 2",
}


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

    @patch("app.main.model.report.Report.get_all_reports")
    def test_get_all_reports(self, mock_get_all_reports):
        # ARRANGE
        data = [report_data_1, report_data_2]
        mock_get_all_reports.return_value = data

        # ACT
        response, status_code = get_all_reports()
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully retrieved reports.")
        self.assertEqual(len(result), len(data))

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["reason"], data[i]["reason"])
            self.assertEqual(result[i]["item_id"], data[i]["item_id"])

        mock_get_all_reports.assert_called_once()

    @patch("app.main.model.report.Report.get_report_by_id")
    def test_get_an_report(self, mock_get_report_by_id):
        # ARRANGE
        data = report_data_1
        mock_get_report_by_id.return_value = data

        # ACT
        response, status_code = get_a_report(
            public_id=generate_fake_public_id(),
            user_id=generate_fake_public_id(),
            role="admin",
        )
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a report.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["item_id"], data["item_id"])

    @patch("app.main.model.report.Report.update_report")
    def test_update_report(self, mock_update_report):
        # ARRANGE
        data = report_data_1
        data["status"] = "accepted"
        mock_update_report.return_value = data

        # ACT
        response, status_code = update_report(
            public_id=generate_fake_public_id(), status="accepted"
        )
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully update report.")
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["status"], data["status"])

        mock_update_report.assert_called_once()

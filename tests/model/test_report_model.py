import uuid
import unittest
from unittest.mock import patch
from app.main import create_app
from app.main.model.report import Report

report_data = {
    "type": "review",
    "item_id": str(uuid.uuid4()),
    "reason": "Test Reason",
}

class TestReport(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")

    @patch('app.main.model.report.db')
    def test_create_and_get_report(self, mock_db):
        # ARRANGE
        report_model = Report()
        mock_db.create_all.return_value = None
        mock_db.session.add.return_value = None
        mock_db.session.commit.return_value = None

        # ACT
        created_report = report_model.create_report(report_data)
        # retrieved_report = report_model.get_report_by_id(created_report["public_id"])

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])

if __name__ == "__main__":
    unittest.main()

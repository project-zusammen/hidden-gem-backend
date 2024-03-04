import uuid
import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

user_data = {
    "id": 1,
    "public_id": str(uuid.uuid4()),
    "username": "test_user",
    "email": "@gmail.com",
    "password": "test_password",
    "role": "user",
    "status": "active",
}

admin_data = {
    "id": 1,
    "public_id": str(uuid.uuid4()),
    "username": "test_user",
    "email": "@gmail.com",
    "password": "test_password",
    "role": "admin",
    "status": "active",
}

report_data = [
    {
        "public_id": str(uuid.uuid4()),
        "user_id": user_data["public_id"],
        "type": "review",
        "item_id": str(uuid.uuid4()),
        "reason": "Test Reason 1",
    },
    {
        "public_id": str(uuid.uuid4()),
        "user_id": user_data["public_id"],
        "type": "review",
        "item_id": str(uuid.uuid4()),
        "reason": "Test Reason 2",
    },
]


error_message = "Input payload validation failed"

public_id = str(uuid.uuid4())


class TestReportEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.report_controller.create_report")
    def test_create_report_success(self, mock_create_report):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": report_data[0],
        }
        mock_create_report.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/report", json=report_data[0], headers=headers)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["type"], res.get("type"))
        self.assertEqual(expected_response["data"]["item_id"], res.get("item_id"))
        self.assertEqual(expected_response["data"]["user_id"], res.get("user_id"))
        self.assertEqual(expected_response["data"]["reason"], res.get("reason"))
        mock_create_report.assert_called_once()

    def test_craete_report_missing_token(self):
        # ARRANGE
        expected_response = {
            "message": "Access Denied: Unauthorized operation. Please log in to proceed."
        }

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/report", json=report_data[0])
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 401)
        self.assertEqual(expected_response["message"], res["message"])

    @patch("app.main.controller.report_controller.create_report")
    def test_create_report_missing_type(self, mock_create_report):
        # ARRANGE
        report_data_single_missing_type = {
            "item_id": "some_item_id",
            "reason": "some_reason",
        }

        expected_response = {
            "message": error_message,
            "errors": {"type": "'type' is a required property"},
            "errors": {"type": "'type' is a required property"},
        }
        mock_create_report.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/report", json=report_data_single_missing_type)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])

        self.assertEqual(expected_response["errors"], res["errors"])

    @patch("app.main.controller.report_controller.create_report")
    def test_create_report_missing_item_id(self, mock_create_report):
        # ARRANGE
        report_data_single_missing_item_id = {
            "type": "review",
            "reason": "some_reason",
        }

        expected_response = {
            "message": error_message,
            "errors": {"item_id": "'item_id' is a required property"},
            "errors": {"item_id": "'item_id' is a required property"},
        }
        mock_create_report.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/report", json=report_data_single_missing_item_id
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])

        self.assertEqual(expected_response["errors"], res["errors"])

    @patch("app.main.controller.report_controller.create_report")
    def test_create_report_missing_reason(self, mock_create_report):
        # ARRANGE
        report_data_single_missing_reason = {
            "type": "review",
            "item_id": "some_item_id",
        }

        expected_response = {
            "message": error_message,
            "errors": {"reason": "'reason' is a required property"},
            "errors": {"reason": "'reason' is a required property"},
        }
        mock_create_report.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/report", json=report_data_single_missing_reason
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])

    @patch("app.main.controller.report_controller.get_all_reports")
    def test_get_all_reports(self, mock_get_all_reports):
        # ARRANGE
        expected_data = report_data
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved reports.",
            "data": expected_data,
        }
        mock_get_all_reports.return_value = expected_response
        page = 1
        count = 2

        token = create_token(admin_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.get(
                f"/api/report?page={page}&count={count}", headers=headers
            )
            res = json.loads(response.data.decode("utf-8"))
            res = res.get("data")
            first_report = res[0]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(res, list)
        self.assertEqual(expected_data[0]["reason"], first_report["reason"])
        mock_get_all_reports.assert_called_once()

    @patch("app.main.controller.report_controller.get_a_report")
    def test_get_a_report(self, mock_get_an_report):
        # ARRANGE
        expected_data = report_data[0]
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved report.",
            "data": expected_data,
        }
        mock_get_an_report.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.get(
                f"/api/report/{report_data[0]['public_id']}", headers=headers
            )
            res = json.loads(response.data.decode("utf-8"))
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_data["reason"], res["reason"])
        mock_get_an_report.assert_called_once()

    @patch("app.main.controller.report_controller.update_report")
    def test_update_report(self, mock_update_report):
        # ARRANGE
        report_data[0]["status"] = "accepted"
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": report_data,
        }
        mock_update_report.return_value = expected_response

        token = create_token(admin_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.put(
                f"/api/report/{public_id}", json=report_data, headers=headers
            )
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["status"], res["status"])

        mock_update_report.assert_called_once()

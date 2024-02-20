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
    "role": "admin",
    "status": "active",
}

report_data = {
    "id": 1,
    "public_id": str(uuid.uuid4()),
    "user_id": user_data["public_id"],
    "type": "review",
    "item_id": str(uuid.uuid4()),
    "reason": "Test Reason",
}

appeal_data_single = {
    "reason": "This is a test appeal.",
    "report_id": report_data["public_id"],
    "user_id": user_data["public_id"],
}

appeal_data_multiple = [
    {
        "reason": "This is a test appeal 1.",
        "report_id": report_data["public_id"],
        "user_id": user_data["public_id"],
    },
    {
        "reason": "This is a test appeal 2.",
        "report_id": report_data["public_id"],
        "user_id": user_data["public_id"],
    },
]

public_id = "public_id_test"


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
            "data": appeal_data_single,
        }
        mock_create_appeal.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/appeal", json=appeal_data_single, headers=headers
            )
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["reason"], res.get("reason"))
        mock_create_appeal.assert_called_once()

    @patch("app.main.controller.appeal_controller.get_all_appeals")
    def test_get_all_appeals(self, mock_get_all_appeals):
        # ARRANGE
        expected_data = [appeal_data_single]
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved appeals.",
            "data": expected_data,
        }
        mock_get_all_appeals.return_value = expected_response
        page = 1
        count = 2

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.get(
                f"/api/appeal?page={page}&count={count}", headers=headers
            )
            res = json.loads(response.data.decode("utf-8"))
            res = res.get("data")
            first_appeal = res[0]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(res, list)
        self.assertEqual(expected_data[0]["reason"], first_appeal["reason"])
        mock_get_all_appeals.assert_called_once()

    @patch("app.main.controller.appeal_controller.get_an_appeal")
    def test_get_an_appeal(self, mock_get_an_appeal):
        # ARRANGE
        expected_data = appeal_data_single
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved appeal.",
            "data": expected_data,
        }
        mock_get_an_appeal.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/appeal/{public_id}", headers=headers)
            res = json.loads(response.data.decode("utf-8"))
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_data["reason"], res["reason"])
        mock_get_an_appeal.assert_called_once()

    @patch("app.main.controller.appeal_controller.update_appeal")
    def test_update_appeal(self, mock_update_appeal):
        # ARRANGE
        appeal_data_single["status"] = "accepted"
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": appeal_data_single,
        }
        mock_update_appeal.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.put(
                f"/api/appeal/{public_id}", json=appeal_data_single, headers=headers
            )
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["status"], res["status"])

        mock_update_appeal.assert_called_once()

import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.appeal_service import create_appeal, get_all_appeals, get_a_appeal, update_appeal


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
        response, status_code = create_appeal(data, user_id=generate_fake_public_id())
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["report_id"], data["report_id"])

        mock_create_appeal.assert_called_once()

    @patch("app.main.model.appeal.Appeal.get_all_appeals")
    def test_get_all_appeals(self, mock_get_all_appeals):
        # ARRANGE
        data = [appeal_1, appeal_2]
        mock_get_all_appeals.return_value = data

        # ACT
        response, status_code = get_all_appeals()
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully retrieved appeals.")
        self.assertEqual(len(result), len(data))

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["reason"], data[i]["reason"])
            self.assertEqual(result[i]["report_id"], data[i]["report_id"])

        mock_get_all_appeals.assert_called_once()

    @patch("app.main.model.appeal.Appeal.get_appeal_by_id")
    def test_get_a_appeal(self, mock_get_appeal_by_id):
        # ARRANGE
        data = appeal_1
        mock_get_appeal_by_id.return_value = data

        # ACT
        response, status_code = get_a_appeal(
            public_id=generate_fake_public_id(),
            user_id=generate_fake_public_id(),
            role="admin",
        )
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a appeal.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["report_id"], data["report_id"])

        mock_get_appeal_by_id.assert_called_once()

    @patch("app.main.model.appeal.Appeal.update_appeal")
    def test_update_appeal(self, mock_update_appeal):
        # ARRANGE
        data = appeal_1
        data["status"] = "accepted"
        mock_update_appeal.return_value = data

        # ACT
        response, status_code = update_appeal(public_id=generate_fake_public_id(), status="accepted")
        result = response["data"]

        # ASSERT
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully update appeal.")
        self.assertEqual(result["reason"], data["reason"])
        self.assertEqual(result["report_id"], data["report_id"])
        self.assertEqual(result["status"], data["status"])

        mock_update_appeal.assert_called_once()

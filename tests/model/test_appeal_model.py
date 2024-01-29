import uuid
import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.appeal import Appeal

appeal_data = {
    "reason": "This is a test appeal.",
    "report_id": "report_id",
}


class TestAppeal(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_appeal(self):
        # ARRANGE
        appeal_model = Appeal()

        # ACT
        new_appeal = appeal_model.create_appeal(appeal_data)

        # ASSERT
        self.assertIsNotNone(new_appeal)
        self.assertEqual(new_appeal["reason"], appeal_data["reason"])

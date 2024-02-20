import uuid
import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.appeal import Appeal
from app.main.model.user import User

appeal_data = {"reason": "This is a test appeal.", "report_id": "report_id"}


def register_user():
    global user_id, user_role
    user_data = {
        "username": "test_user",
        "email": "test_user@gmail.com",
        "password": "test_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    user_id = user_model.get_user_id(user["public_id"])
    user_role = user_model.get_user_role(user["role"])


def register_admin():
    global admin_id, admin_role
    user_data = {
        "username": "test_admin",
        "email": "test_admin@gmail.com",
        "password": "test_admin_password",
    }
    user_model = User()
    admin = user_model.register_admin(user_data)
    admin_id = user_model.get_user_id(admin["public_id"])
    admin_role = user_model.get_user_role(admin["public_id"])


class TestAppeal(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        register_user()
        register_admin()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_appeal(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = user_id

        # ACT
        new_appeal = appeal_model.create_appeal(appeal_data)

        # ASSERT
        self.assertIsNotNone(new_appeal)
        self.assertEqual(new_appeal["reason"], appeal_data["reason"])

    def test_get_all_appeals(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = user_id
        appeal_model.create_appeal(appeal_data)
        page = 1
        count = 2

        # ACT
        all_appeals = appeal_model.get_all_appeals(page, count)

        # ASSERT
        self.assertIsNotNone(all_appeals)
        self.assertEqual(all_appeals[0]["reason"], appeal_data["reason"])

    def test_get_appeal_by_id_role_admin(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = admin_id
        appeal = appeal_model.create_appeal(appeal_data)

        # ACT
        retrieved_appeal = appeal_model.get_appeal_by_id(
            public_id=appeal["public_id"], user_id=admin_id, role=admin_role
        )

        # ASSERT
        self.assertIsNotNone(retrieved_appeal)
        self.assertEqual(retrieved_appeal["reason"], appeal_data["reason"])

    def test_get_appeal_by_id_role_user(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = user_id
        appeal = appeal_model.create_appeal(appeal_data)

        # ACT
        retrieved_appeal = appeal_model.get_appeal_by_id(
            public_id=appeal["public_id"], user_id=user_id, role=user_role
        )

        # ASSERT
        self.assertIsNotNone(retrieved_appeal)
        self.assertEqual(retrieved_appeal["reason"], appeal_data["reason"])

    def test_get_appeal_failed(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = admin_id
        appeal = appeal_model.create_appeal(appeal_data)

        # ACT

        # ASSERT
        with self.assertRaises(Exception) as context:
            appeal_model.get_appeal_by_id(
                public_id=appeal["public_id"], user_id=user_id, role=user_role
            )

        self.assertTrue("Access Denied" in str(context.exception))

    def test_update_appeal(self):
        # ARRANGE
        appeal_model = Appeal()
        appeal_data["user_id"] = user_id
        appeal = appeal_model.create_appeal(appeal_data)

        # ACT
        updated_appeal = appeal_model.update_appeal(
            public_id=appeal["public_id"], status="accepted"
        )

        # ASSERT
        self.assertIsNotNone(updated_appeal)
        self.assertEqual(updated_appeal["status"], "accepted")


if __name__ == "__main__":
    unittest.main()

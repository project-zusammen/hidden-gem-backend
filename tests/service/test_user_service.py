import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.user_service import (
    get_all_users,
    get_a_user,
    register_user,
    delete_user,
    updated_user,
    updated_user_status
)

def generate_fake_public_id():
    return str(uuid.uuid4())

class TestUserService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.user.User.get_all_users")
    def test_get_all_users(self, mock_get_all_users):
        # Arrange
        public_id_1 = generate_fake_public_id()
        public_id_2 = generate_fake_public_id()
        data = [
            {
                "public_id": public_id_1,
                "username": "ikan tenggiri",
                "email": "tenggiri@gmail.com",
                "role": "user",
                "status": "active"
            },
            {
                "public_id": public_id_2,
                "username": "ikan gabus",
                "email": "gabus@gmail.com",
                "role": "user",
                "status": "active"
            }
        ]
        mock_get_all_users.return_value = data

        # Act
        response, status_code = get_all_users()
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully retrieved users.")
        self.assertEqual(len(result), len(data))

        mock_get_all_users.assert_called_once()

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["username"], data[i]["username"])
            self.assertEqual(result[i]["email"], data[i]["email"])
            self.assertEqual(result[i]["role"], data[i]["role"])
            self.assertEqual(result[i]["status"], data[i]["status"])

    @patch("app.main.model.user.User.get_user_by_id")
    def test_get_a_user(self, mock_get_user_by_id):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "username": "ikan tenggiri",
            "email": "tenggiri@gmail.com",
            "role": "user",
            "status": "active"
        }
        mock_get_user_by_id.return_value = data

        # Act
        response, status_code = get_a_user(public_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a user.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["username"], data["username"])
        self.assertEqual(result["role"], data["role"])
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["status"], data["status"])

    @patch("app.main.model.user.User.register_user")
    def test_register_user(self, mock_register_user):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "username": "ikan tenggiri",
            "email": "tenggiri@gmail.com",
            "role": "user",
            "status": "active"
        }
        mock_register_user.return_value = data

        # Act
        response, status_code = register_user(data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Register User Success.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["username"], data["username"])
        self.assertEqual(result["role"], data["role"])
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["status"], data["status"])

    @patch("app.main.model.user.User.update_user")
    def test_update_user(self, mock_update_user):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "username": "ikan tenggiri",
            "email": "tenggiri@gmail.com",
            "role": "user",
            "status": "active"
        }
        mock_update_user.return_value = data

        # Act
        response, status_code = updated_user(public_id, data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully update user")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["username"], data["username"])
        self.assertEqual(result["role"], data["role"])
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["status"], data["status"])
    
    @patch("app.main.model.user.User.update_user_status")
    def test_update_user(self, mock_update_user_status):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "username": "ikan tenggiri",
            "email": "tenggiri@gmail.com",
            "role": "user",
            "status": "inactive"
        }
        mock_update_user_status.return_value = data

        # Act
        response, status_code = updated_user_status(public_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully update status user")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["username"], data["username"])
        self.assertEqual(result["role"], data["role"])
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["status"], data["status"])

    @patch("app.main.model.user.User.delete_user")
    def test_delete_user(self, mock_delete_user):
        # Arrange
        public_id = generate_fake_public_id()
        mock_delete_user.return_value = True

        # Act
        response, status_code = delete_user(public_id)

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully delete user")

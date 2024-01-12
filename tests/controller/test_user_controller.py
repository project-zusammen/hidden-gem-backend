import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

user_data = {
    "username": "aqiz",
    "email": "aqiz@gmail.com",
    "password": "Aqiz123!"
}

class TestUserEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.user_controller.register_user")
    def test_user_signup(self, mock_register_user):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Register User Success.",
            "data": user_data,
        }
        mock_register_user.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/user/signup", json=user_data)
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"], res)
        mock_register_user.assert_called_once_with(user_data)


    @patch("app.main.controller.user_controller.get_all_users")
    def test_get_all_users_success(self, mock_get_all_users):
        # ARRANGE
        expected_data = [{
            "id" : 1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "created_at": "2024-01-03T11:21:23",
            "updated_at": "2024-01-03T11:21:23",
            "role": "user",
            "status": "active"
            }
        ]
        expected_response = {
            "status": "success",
            "message": "Successfully get users.",
            "data": expected_data,
        }

        mock_get_all_users.return_value = expected_response
        token = create_token(expected_data[0])
        
        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/user", headers={"X-API-KEY":token})
            result = response.get_json()["data"]

            first_user = result[0]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(first_user.get("username"), expected_data[0].get("username"))
        self.assertEqual(first_user.get("email"), expected_data[0].get("email"))
        self.assertEqual(first_user.get("role"), expected_data[0].get("role"))
        self.assertEqual(first_user.get("status"), expected_data[0].get("status"))
        self.assertEqual(first_user.get("public_id"), expected_data[0].get("public_id"))
        mock_get_all_users.assert_called_once()


    @patch("app.main.controller.user_controller.get_a_user")
    def test_get_a_user(self, mock_get_a_user):
        # ARRANGE
        public_id = "c47560e6-619f-4867-8ea7-213709aea349"
        expected_data = [{
            "id":1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "created_at": "2024-01-03T11:21:23",
            "updated_at": "2024-01-03T11:21:23",
            "role": "user",
            "status": "active"
            }
        ]
        expected_response = {
            "status": "success",
            "message": "Successfully get a user.",
            "data": expected_data,
        }
        mock_get_a_user.return_value = expected_response
        token = create_token(expected_data[0])

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/user/{public_id}", headers={"X-API-KEY":token})
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get("username"), res.get("username"))
        self.assertEqual(expected_response.get("email"), res.get("email"))
        self.assertEqual(expected_response.get("role"), res.get("role"))
        self.assertEqual(expected_response.get("status"), res.get("status"))
        self.assertEqual(expected_response.get("public_id"), res.get("public_id"))

    @patch("app.main.controller.user_controller.update_user")
    def test_update_user(self, mock_update_user):
        # ARRANGE
        public_id = "test-public-id"
        token_payload = {
            "id":1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "role": "user",
            "status": "active"
        }
        expected_response = {
            "status": "success",
            "message": "Successfully update user",
            "data": user_data,
        }
        mock_update_user.return_value = expected_response
        token = create_token(token_payload)

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/user/{public_id}", json=user_data, headers={"X-API-KEY":token})
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response['data']["username"], res.get("username"))
        self.assertEqual(expected_response['data']["email"], res.get("email"))
        mock_update_user.assert_called_once()

    @patch("app.main.controller.user_controller.delete_user")
    def test_delete_user(self, mock_delete_user):
        # ARRANGE
        token_payload = {
            "id":1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "role": "user",
            "status": "active"
        }
        expected_response = {
            "status": "success",
            "message": "Successfully delete user",
        }
        mock_delete_user.return_value = expected_response
        token = create_token(token_payload)

        # ACT
        with self.app.test_client() as client:
            response = client.delete(f"/api/user/{token_payload['public_id']}",headers={"X-API-KEY":token})
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get("status"), res.get("status"))
        self.assertEqual(expected_response.get("message"), res.get("message"))
        mock_delete_user.assert_called_once()

    @patch("app.main.controller.user_controller.update_user_status")
    def test_update_user_status(self, mock_update_user):
        # ARRANGE
        expected_data = {
            "id":1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "created_at": "2024-01-03T11:21:23",
            "updated_at": "2024-01-03T11:21:23",
            "role": "admin",
            "status": "active"
        }
        public_id = expected_data['public_id']
        update_status_payload = {
            "banned" : True,
        }
        expected_response = {
            "status": "success",
            "message": "Successfully update user status",
            "data": user_data,
        }
        mock_update_user.return_value = expected_response
        token = create_token(expected_data)

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/user/{public_id}/status", json=update_status_payload, headers={"X-API-KEY":token})
            res = response.get_json()["data"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response['data']["username"], res.get("username"))
        self.assertEqual(expected_response['data']["email"], res.get("email"))
        mock_update_user.assert_called_once()

    @patch("app.main.controller.user_controller.user_auth")
    def test_user_auth(self, mock_user_auth):
        # ARRANGE
        expected_data = {
            "id":1,
            "public_id": "c47560e6-619f-4867-8ea7-213709aea349",
            "username": "aqiz",
            "email": "aqiz@gmail.com",
            "password": "password",
            "role": "admin",
            "status": "active"
        }
        token = create_token(expected_data)
        user_credential = {
            "email" : expected_data['email'],
            "password": expected_data['password']
        }
        expected_response = {
            "status": "success",
            "message": "Login Success",
            "token": token,
        }
        mock_user_auth.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/user/login", json=user_credential)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res['status'])
        self.assertEqual(expected_response["message"], res['message'])
        self.assertEqual(expected_response["token"], res['token'])
        mock_user_auth.assert_called_once_with(user_credential)
    
    
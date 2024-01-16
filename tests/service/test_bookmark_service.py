import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token
from app.main.service.bookmark_service import (
    create_bookmark,
    get_bookmark_by_userid,
    delete_bookmark
)

def generate_fake_public_id():
    return str(uuid.uuid4())

class TestBookmarkService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.bookmark.Bookmark.get_bookmark_by_userid")
    def test_get_bookmark_by_userid(self, mock_get_bookmark_by_userid):
        # Arrange
        user_id = 1
        data = [
            {
            "public_id": "ec064187-a837-4f75-b22a-0b6ee6136a7e",
            "user_id": "000f59b8-96fb-4db8-86ec-3a8d956466a7",
            "review_id": "c0430443-4296-4b6c-ba4c-553ddd5104f5",
            "created_at": "2024-01-16T03:01:20",
            "updated_at": "2024-01-16T03:01:20"
            },
            {
            "public_id": "4306e51c-8715-4c62-aae2-ffd86a4b5794",
            "user_id": "000f59b8-96fb-4db8-86ec-3a8d956466a7",
            "review_id": "4128525d-7851-4562-839d-ff0479384508",
            "created_at": "2024-01-16T03:13:22",
            "updated_at": "2024-01-16T03:13:22"
            }
        ]
        mock_get_bookmark_by_userid.return_value = data

        # Act
        response, status_code = get_bookmark_by_userid(user_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a bookmark.")
        self.assertEqual(len(result), len(data))

        mock_get_bookmark_by_userid.assert_called_once()

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["user_id"], data[i]["user_id"])
            self.assertEqual(result[i]["review_id"], data[i]["review_id"])

    @patch("app.main.model.bookmark.Bookmark.create_bookmark")
    def test_create_bookmark(self, mock_create_bookmark):
        # Arrange
        data = {
            "user_id": "66434932-de79-4800-955a-fa09466c5218",
            "review_id": "4128525d-7851-4562-839d-ff0479384508"
        }
        mock_create_bookmark.return_value = data

        # Act
        response, status_code = create_bookmark(data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["user_id"], data["user_id"])
        self.assertEqual(result["review_id"], data["review_id"])
        mock_create_bookmark.assert_called_once()

    @patch("app.main.model.bookmark.Bookmark.delete_bookmark")
    def test_delete_bookmark(self, mock_delete_bookmark):
        # Arrange
        public_id = generate_fake_public_id()
        user_id = 1
        mock_delete_bookmark.return_value = True

        # Act
        response, status_code = delete_bookmark(public_id,user_id)

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully deleted.")
        mock_delete_bookmark.assert_called_once()

   
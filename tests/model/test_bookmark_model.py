import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.bookmark import Bookmark
from app.main.model.user import User
from app.main.model.review import Review
from app.main.util.helper import create_token


review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
}
user_data = {
    "username": "aqiz",
    "email": "aqiz@gmail.com",
    "password": "Aqiz123!"
}

class TestBookmark(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_bookmark(self):
        # ARRANGE
        review_model = Review()
        created_review = review_model.create_review(review_data)
        user_model = User()
        new_user = user_model.register_user(user_data)
        bookmark_data = {
            "user_id": new_user['public_id'],
            "review_id": created_review['public_id']
        }
        bookmark_model = Bookmark()
        new_bookmark = bookmark_model.create_bookmark(bookmark_data)

        # ASSERT
        self.assertIsNotNone(new_bookmark)
        self.assertEqual(new_bookmark["user_id"], bookmark_data["user_id"])
        self.assertEqual(new_bookmark["review_id"], bookmark_data["review_id"])

    def test_get_bookmark_by_userid(self):
        # ARRANGE
        review_model = Review()
        created_review = review_model.create_review(review_data)
        user_model = User()
        new_user = user_model.register_user(user_data)
        bookmark_data = {
            "user_id": new_user['public_id'],
            "review_id": created_review['public_id']
        }
        bookmark_model = Bookmark()
        new_boomark = bookmark_model.create_bookmark(bookmark_data)

        # ACT
        retrieved_bookmark = bookmark_model.get_bookmark_by_userid(bookmark_data['user_id'])

        # ASSERT
        self.assertIsNotNone(retrieved_bookmark)
        self.assertEqual(len(retrieved_bookmark), 1)
        self.assertEqual(new_boomark["review_id"], retrieved_bookmark[0]["review_id"])
        self.assertEqual(new_boomark["user_id"], retrieved_bookmark[0]["user_id"])
        self.assertEqual(new_boomark["public_id"], retrieved_bookmark[0]["public_id"])

    def test_delete_user(self):
        # ARRANGE
        review_model = Review()
        created_review = review_model.create_review(review_data)
        user_model = User()
        new_user = user_model.register_user(user_data)
        bookmark_data = {
            "user_id": new_user['public_id'],
            "review_id": created_review['public_id']
        }
        bookmark_model = Bookmark()
        new_bookmark = bookmark_model.create_bookmark(bookmark_data)

        # ACT
        deleted_bookmark = bookmark_model.delete_bookmark(new_bookmark['public_id'],1)

        # ASSERT
        self.assertIsNotNone(deleted_bookmark)
        self.assertEqual(deleted_bookmark,True)

    
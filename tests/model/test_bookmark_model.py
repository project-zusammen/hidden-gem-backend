import unittest
import datetime
from app.main import create_app
from app.extensions import db
from app.main.model.bookmark import Bookmark
from app.main.model.user import User
from app.main.model.review import Review
from app.main.model.region import Region

def create_review_and_user():
    global review, user
    
    region = Region(
        public_id = "region_id",
        city = "Test Region",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    region.save()

    user = User(
        username = "test_user",
        email = "test_user@gmail.com",
        password = "test_user_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    user.save()

    review = Review(
        public_id = "review_id",
        user_id = user.id,
        title = "Test Review",
        content = "This is a test review.",
        location = "Test Location",
        region_id = region.id,
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
        upvotes = 0,
        downvotes = 0,
        visible = True,
    )
    review.save()


class TestBookmark(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        create_review_and_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_bookmark(self):
        # ARRANGE
        bookmark_model = Bookmark()
        new_bookmark = bookmark_model.create_bookmark(review.public_id, user.id)

        # ASSERT
        self.assertIsNotNone(new_bookmark)
        self.assertEqual(new_bookmark["user_id"], user.public_id)
        self.assertEqual(new_bookmark["review_id"], review.public_id)

    def test_get_bookmark_by_userid(self):
        # ARRANGE
        bookmark_model = Bookmark()
        new_bookmark = bookmark_model.create_bookmark(review.public_id, user.id)

        # ACT
        retrieved_bookmark = bookmark_model.get_bookmark_by_userid(user.id)

        # ASSERT
        self.assertIsNotNone(retrieved_bookmark)
        self.assertEqual(len(retrieved_bookmark), 1)
        self.assertEqual(new_bookmark["review_id"], retrieved_bookmark[0]["review_id"])
        self.assertEqual(new_bookmark["user_id"], retrieved_bookmark[0]["user_id"])
        self.assertEqual(new_bookmark["public_id"], retrieved_bookmark[0]["public_id"])

    def test_delete_bookmark(self):
        # ARRANGE
        bookmark_model = Bookmark()
        new_bookmark = bookmark_model.create_bookmark(review.public_id, user.id)

        # ACT
        deleted_bookmark = bookmark_model.delete_bookmark(new_bookmark["public_id"], user.id)

        # ASSERT
        self.assertIsNotNone(deleted_bookmark)
        self.assertTrue(deleted_bookmark)

if __name__ == "__main__":
    unittest.main()

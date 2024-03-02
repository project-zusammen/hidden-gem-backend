import uuid
import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.comment import Comment
from app.main.model.review import Review
from app.main.model.region import Region
from app.main.model.user import User
from app.main.model.tag import Tag

comment_data = {"content": "new comment"}
tag_data = {"tag": "new tag"}

def create_region(region_name="Test Region"):
    region_model = Region()
    region = region_model.create_region(region_name)
    region_id = region["public_id"]
    return region_id

def create_tag():
    tag_model = Tag()
    tag = tag_model.create_tag(tag_data)
    tag_id = tag["public_id"]
    return tag_id

def create_user():
    user_model = User()
    user_data = {
        "username": "test_user",
        "email": "test_user@gmail.com",
        "password": "test_password"
    }
    user = user_model.register_user(user_data)
    return user["public_id"]

def create_review():
    global review_id
    region_id = create_region()
    user_id = create_user()
    tag_id = create_tag()
    review_data = {
        "title": "Test Review",
        "content": "This is a test review.",
        "location": "Test Location",
        "region_id": region_id,
        "user_id": user_id,
        "tag_id": tag_id,
    }

    review_model = Review()
    review = review_model.create_review(review_data)
    review_id = review["public_id"]

class TestComment(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        create_review()
        comment_data["review_id"] = review_id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_comment(self):
        # ARRANGE
        comment_model = Comment()

        # ACT
        new_comment = comment_model.create_comment(comment_data)

        # ASSERT
        self.assertIsNotNone(new_comment)
        self.assertEqual(new_comment["content"], comment_data["content"])

    def test_get_all_comments(self):
        # ARRANGE
        comment_model = Comment()
        comment_model.create_comment(comment_data)

        # ACT
        retrieved_comments = comment_model.get_all_comments()

        # ASSERT
        self.assertIsNotNone(retrieved_comments)
        self.assertEqual(comment_data["content"], retrieved_comments[0]["content"])

    def test_get_comment_by_id(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

        # ACT
        retrieved_comment = comment_model.get_comment_by_id(
            public_id=comment["public_id"]
        )

        # ASSERT
        self.assertIsNotNone(retrieved_comment)
        self.assertEqual(comment_data["content"], retrieved_comment["content"])

    def test_delete_comment(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

        # ACT
        deleted_comment = comment_model.delete_comment(public_id=comment["public_id"])

        # ASSERT
        self.assertIsNotNone(deleted_comment)
        self.assertFalse(deleted_comment["visible"])

    def test_update_comment(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

        # ACT
        updated_data = {"content": "updated comment"}
        updated_comment = comment_model.update_comment(
            comment["public_id"], updated_data
        )

        # ASSERT
        self.assertIsNotNone(updated_comment)
        self.assertEqual(comment["public_id"], updated_comment["public_id"])
        self.assertEqual(updated_data["content"], updated_comment["content"])

    def test_upvote_comment(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

        # ACT
        comment_model.upvote_comment(
            comment["public_id"], upvote=True
        )
        upvoted_comment = comment_model.upvote_comment(
            comment["public_id"], upvote=False
        )

        # ASSERT
        self.assertIsNotNone(upvoted_comment)
        self.assertEqual(comment["upvotes"] + 1, upvoted_comment["upvotes"])
        self.assertEqual(comment["downvotes"] + 1, upvoted_comment["downvotes"])

    def test_update_visibility(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

        # ACT
        updated_comment = comment_model.update_visibility(
            comment["public_id"], visible=False
        )

        # ASSERT
        self.assertIsNotNone(updated_comment)
        self.assertFalse(updated_comment["visible"])


if __name__ == "__main__":
    unittest.main()

import datetime
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

def setup_data():
    global review, commenter

    region = Region(
        public_id = "region_id",
        city = "Test Region City",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    region.save()

    reviewer = User(
        username = "test_reviewer",
        email = "test_reviewer@gmail.com",
        password = "test_reviewer_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    reviewer.save()

    review = Review(
        public_id = "review_id",
        user_id = reviewer.id,
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

    commenter = User(
        username = "test_commenter",
        email = "test_commenter@gmail.com",
        password = "test_commenter_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    commenter.save()


class TestComment(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        setup_data()
        comment_data["review_id"] = review.public_id

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
        self.assertEqual(new_comment["review_id"], review.public_id)
        self.assertEqual(new_comment["upvotes"], 0)
        self.assertEqual(new_comment["downvotes"], 0)
        self.assertTrue(new_comment["visible"])

    def test_get_all_comments(self):
        # ARRANGE
        comment_model = Comment()
        comment_model.create_comment(comment_data)

        comment_data_1 = comment_data.copy()
        comment_data_1["content"] = "another comment"
        comment_model.create_comment(comment_data_1)

        comment_data_2 = comment_data.copy()
        comment_data_2["content"] = "yet another comment"
        comment_model.create_comment(comment_data_2)

        # ACT
        retrieved_comments = comment_model.get_all_comments()

        # ASSERT
        self.assertIsNotNone(retrieved_comments)
        self.assertEqual(comment_data["content"], retrieved_comments[0]["content"])
        self.assertEqual(comment_data_1["content"], retrieved_comments[1]["content"])
        self.assertEqual(comment_data_2["content"], retrieved_comments[2]["content"])

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

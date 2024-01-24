import uuid
import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.comment import Comment

comment_data = {"content": "new comment", "review_id": "review_id"}


class TestComment(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_comment(self):
        # ARRANGE
        comment_model = Comment()
        new_comment = comment_model.create_comment(comment_data)

        # ACT

        # ASSERT
        self.assertIsNotNone(new_comment)
        self.assertEqual(new_comment["content"], comment_data["content"])

    def test_get_all_comments(self):
        # ARRANGE
        comment_model = Comment()
        comment = comment_model.create_comment(comment_data)

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
        upvoted_comment = comment_model.upvote_comment(
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

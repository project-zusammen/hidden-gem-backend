import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.review import Review

review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
}


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_review(self):
        # ARRANGE
        review_model = Review()
        created_review = review_model.create_review(review_data)

        # ACT
        retrieved_review = review_model.get_review_by_id(created_review["public_id"])
        retrieved_review = retrieved_review.serialize()

        # ASSERT
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(created_review["title"], retrieved_review["title"])
        self.assertEqual(created_review["content"], retrieved_review["content"])
        self.assertEqual(created_review["location"], retrieved_review["location"])

    def test_update_review(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        updated_data = {
            "title": "Updated Review",
            "content": "This is an updated review.",
            "location": "Updated Location",
        }
        updated_review = review_model.update_review(review["public_id"], updated_data)

        # ASSERT
        self.assertIsNotNone(updated_review)
        self.assertEqual(review["public_id"], updated_review["public_id"])
        self.assertEqual(updated_data["title"], updated_review["title"])
        self.assertEqual(updated_data["content"], updated_review["content"])
        self.assertEqual(updated_data["location"], updated_review["location"])

    def test_get_all_reviews(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        retrieved_reviews = review_model.get_all_reviews()

        # ASSERT
        self.assertIsNotNone(retrieved_reviews)
        self.assertEqual(len(retrieved_reviews), 1)
        self.assertEqual(review["title"], retrieved_reviews[0]["title"])
        self.assertEqual(review["content"], retrieved_reviews[0]["content"])
        self.assertEqual(review["location"], retrieved_reviews[0]["location"])

    def test_delete_review(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        deleted_review = review_model.delete_review(review["public_id"])

        # ASSERT
        self.assertIsNotNone(deleted_review)
        self.assertFalse(deleted_review["visible"])

    def test_upvote_review(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        upvoted_review = review_model.upvote_review(review["public_id"])

        # ASSERT
        self.assertIsNotNone(upvoted_review)
        self.assertEqual(review["upvotes"] + 1, upvoted_review["upvotes"])
        self.assertEqual(review["downvotes"], upvoted_review["downvotes"])

    def test_downvote_review(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        downvoted_review = review_model.upvote_review(
            public_id=review["public_id"], upvote=False
        )

        # ASSERT
        self.assertIsNotNone(downvoted_review)
        self.assertEqual(review["upvotes"], downvoted_review["upvotes"])
        self.assertEqual(review["downvotes"] + 1, downvoted_review["downvotes"])

    def test_update_visibility(self):
        # ARRANGE
        review_model = Review()
        review = review_model.create_review(review_data)

        # ACT
        updated_review = review_model.update_visibility(
            public_id=review["public_id"], visible=False
        )

        # ASSERT
        self.assertIsNotNone(updated_review)
        self.assertFalse(updated_review["visible"])


if __name__ == "__main__":
    unittest.main()

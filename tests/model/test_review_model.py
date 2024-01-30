import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.review import Review
from app.main.model.region import Region
from app.main.model.category import Category
from app.main.model.user import User

review_data = {
    "title": "Test Review",
    "content": "This is a test review #review",
    "location": "Test Location",
    "user_id": 1,
    "region_id": 1,
    "category_id": 1,
}
user_data = {"username": "aqiz", "email": "aqiz@gmail.com", "password": "Aqiz123!"}


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
        region_model = Region()
        category_model = Category()
        user_model = User()

        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
        created_review = review_model.create_review(review_data)

        # ACT
        retrieved_review = review_model.get_review_by_id(created_review["public_id"])
        retrieved_review = retrieved_review.serialize()

        # ASSERT
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(created_review["title"], retrieved_review["title"])
        self.assertEqual(created_review["content"], retrieved_review["content"])
        self.assertEqual(created_review["location"], retrieved_review["location"])
        self.assertEqual(created_review["user_id"], retrieved_review["user_id"])
        self.assertEqual(created_review["region_id"], retrieved_review["region_id"])
        self.assertEqual(created_review["category_id"], retrieved_review["category_id"])

    def test_update_review(self):
        # ARRANGE
        review_model = Review()
        region_model = Region()
        category_model = Category()
        user_model = User()

        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
        created_review = review_model.create_review(review_data)

        # ACT
        updated_data = {
            "title": "Updated Review",
            "content": "This is an updated review.",
            "location": "Updated Location",
            "category_id": 1,
            "region_id": 1,
        }
        updated_review = review_model.update_review(
            created_review["public_id"], updated_data
        )

        # ASSERT
        self.assertIsNotNone(updated_review)
        self.assertEqual(created_review["public_id"], updated_review["public_id"])
        self.assertEqual(updated_data["title"], updated_review["title"])
        self.assertEqual(updated_data["content"], updated_review["content"])
        self.assertEqual(updated_data["location"], updated_review["location"])

    def test_get_all_reviews(self):
        # ARRANGE
        review_model = Review()
        region_model = Region()
        category_model = Category()
        user_model = User()

        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("jakarta")
        created_category = category_model.create_category("food")
        review_data1 = {
            "title": "Test Review1",
            "content": "This is a test review #review1",
            "location": "Test Locatio1",
            "user_id": 1,
            "region_id": 1,
            "category_id": 1,
        }
        review = review_model.create_review(review_data1)

        # ACT
        page = 1
        count = 1
        tag_id = 0
        category_id = 1
        region_id = 1
        retrieved_reviews = review_model.get_all_reviews(
            page, count, tag_id, category_id, region_id
        )

        # ASSERT
        self.assertIsNotNone(retrieved_reviews)
        self.assertEqual(len(retrieved_reviews), 1)
        self.assertEqual(review["title"], retrieved_reviews[0]["title"])
        self.assertEqual(review["content"], retrieved_reviews[0]["content"])
        self.assertEqual(review["location"], retrieved_reviews[0]["location"])

    def test_delete_review(self):
        # ARRANGE
        review_model = Review()
        region_model = Region()
        category_model = Category()
        user_model = User()
        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
        review = review_model.create_review(review_data)

        # ACT
        deleted_review = review_model.delete_review(review["public_id"])

        # ASSERT
        self.assertIsNotNone(deleted_review)
        self.assertFalse(deleted_review["visible"])

    def test_upvote_review(self):
        # ARRANGE
        review_model = Review()
        region_model = Region()
        category_model = Category()
        user_model = User()
        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
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
        region_model = Region()
        category_model = Category()
        user_model = User()
        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
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
        region_model = Region()
        category_model = Category()
        user_model = User()
        created_user = user_model.register_user(user_data)
        created_region = region_model.create_region("purbalingga")
        created_category = category_model.create_category("food")
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

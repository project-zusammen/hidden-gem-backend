import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.review_service import (
    create_review,
    update_review,
    upvote_review,
    update_visibility,
    get_all_reviews,
    get_a_review,
    delete_review,
)


def generate_fake_public_id():
    return str(uuid.uuid4())


class TestReviewService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.review.Review.get_all_reviews")
    def test_get_all_reviews(self, mock_get_all_reviews):
        # Arrange
        public_id_1 = generate_fake_public_id()
        public_id_2 = generate_fake_public_id()
        data = [
            {
                "public_id": public_id_1,
                "title": "Test Review 1",
                "content": "Content 1",
                "location": "Location 1",
            },
            {
                "public_id": public_id_2,
                "title": "Test Review 2",
                "content": "Content 2",
                "location": "Location 2",
            },
        ]
        mock_get_all_reviews.return_value = data

        # Act
        response, status_code = get_all_reviews()
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully retrieved reviews.")
        self.assertEqual(len(result), len(data))

        mock_get_all_reviews.assert_called_once()

        for i in range(len(result)):
            self.assertEqual(result[i]["public_id"], data[i]["public_id"])
            self.assertEqual(result[i]["title"], data[i]["title"])
            self.assertEqual(result[i]["content"], data[i]["content"])
            self.assertEqual(result[i]["location"], data[i]["location"])

    @patch("app.main.model.review.Review.get_review_by_id")
    def test_get_a_review(self, mock_get_review_by_id):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "title": "Test Review",
            "content": "This is a content review",
            "location": "Test Location",
        }
        mock_get_review_by_id.return_value = data

        # Act
        response, status_code = get_a_review(public_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully get a review.")
        self.assertEqual(result["public_id"], data["public_id"])
        self.assertEqual(result["title"], data["title"])
        self.assertEqual(result["content"], data["content"])
        self.assertEqual(result["location"], data["location"])

    @patch("app.main.model.review.Review.create_review")
    # @patch("app.main.model.review.Review.get_review_id_by_public_id")
    # @patch("app.main.model.review.Review.get_the_hashtag_from_content")
    # @patch("app.main.model.tag.Tag.create_tag")
    # @patch("app.main.model.tag.ReviewTag.create_review_tag")
    def test_create_review(
        self,
        # mock_create_review_tag,
        # mock_create_tag,
        # mock_get_hashtags,
        # mock_get_review_id,
        mock_create_review,
    ):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "title": "Test Review",
            "content": "This is a content review #tag1 #tag2",
            "location": "Test Location",
        }
        # tag_data = {"id": 1, "public_id": public_id, "name": "#tag1"}
        # review_tag_data = {"id": 1, "public_id": public_id, "tag_id": 1, "review_id": 1}
        mock_create_review.return_value = data
        # mock_get_review_id.return_value = 1
        # mock_get_hashtags.return_value = ["#tag1"]
        # mock_create_tag.return_value = tag_data
        # mock_create_review_tag.return_value = review_tag_data

        # Act
        response, status_code = create_review(data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully created.")
        self.assertEqual(result["title"], data["title"])
        self.assertEqual(result["content"], data["content"])
        self.assertEqual(result["location"], data["location"])

        # Check interactions with mock methods
        mock_create_review.assert_called_once_with(data)
        # mock_get_review_id.assert_called_once_with(public_id)
        # mock_get_hashtags.assert_called_once_with(data["content"])

    @patch("app.main.model.review.Review.update_review")
    def test_update_review(self, mock_update_review):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "title": "Test Review updated",
            "content": "This is a content review updated",
            "location": "Test Location updated",
        }
        data["public_id"] = public_id
        mock_update_review.return_value = data

        # Act
        response, status_code = update_review(public_id, data)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully updated.")
        self.assertEqual(result["title"], data["title"])
        self.assertEqual(result["content"], data["content"])
        self.assertEqual(result["location"], data["location"])

    @patch("app.main.model.review.Review.upvote_review")
    def test_upvote_review(self, mock_upvote_review):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "title": "Test Review",
            "content": "This is a content review",
            "location": "Test Location",
            "upvotes": 1,
            "downvotes": 0,
        }
        mock_upvote_review.return_value = data

        # Act
        response, status_code = upvote_review(public_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully upvoted.")
        self.assertEqual(result["upvotes"], data["upvotes"])
        self.assertEqual(result["downvotes"], data["downvotes"])

    @patch("app.main.model.review.Review.update_visibility")
    def test_update_visibility(self, mock_update_visibility):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "title": "Test Review",
            "content": "This is a content review",
            "location": "Test Location",
            "visible": False,
        }
        mock_update_visibility.return_value = data

        # Act
        response, status_code = update_visibility(public_id, False)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully updated.")
        self.assertEqual(result["visible"], data["visible"])

    @patch("app.main.model.review.Review.delete_review")
    def test_delete_review(self, mock_delete_review):
        # Arrange
        public_id = generate_fake_public_id()
        data = {
            "public_id": public_id,
            "title": "Test Review",
            "content": "This is a content review",
            "location": "Test Location",
            "visible": False,
        }
        mock_delete_review.return_value = data

        # Act
        response, status_code = delete_review(public_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Successfully deleted.")
        self.assertEqual(result["visible"], data["visible"])

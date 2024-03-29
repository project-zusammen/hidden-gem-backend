import os
import uuid
import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

os.environ["DEBUG"] = "True"

review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
    "region_id": "test-region-id",
    "category_id": "test-category-id",
    "tag_id": "test-tag-id",
    "image_urls": ["test-image-url-1", "test-image-url-2"],
}

error_message = "Input payload validation failed"

user_data = {
    "id": 1,
    "public_id": str(uuid.uuid4()),
    "username": "test_user",
    "email": "@gmail.com",
    "password": "test_password",
    "role": "user",
    "status": "active",
}

class TestReviewEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.review_controller.create_review")
    def test_create_review(self, mock_create_review):
        # ARRANGE
        expected_response = {
            "status": "success",
            "message": "Successfully created.",
            "data": review_data,
        }
        mock_create_review.return_value = expected_response

        token = create_token(user_data)
        headers = {"X-API-KEY": token}

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/review", json=review_data, headers=headers)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["title"], res.get("title"))
        self.assertEqual(expected_response["data"]["content"], res.get("content"))
        self.assertEqual(expected_response["data"]["location"], res.get("location"))
        self.assertEqual(expected_response["data"]["region_id"], res.get("region_id"))
        self.assertEqual(expected_response["data"]["category_id"], res.get("category_id"))
        self.assertEqual(expected_response["data"]["tag_id"], res.get("tag_id"))
        self.assertEqual(
            expected_response["data"]["image_urls"], res.get("image_urls")
        )
        mock_create_review.assert_called_once()

    @patch("app.main.controller.review_controller.get_all_reviews")
    def test_get_all_reviews(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {"title": "Review 1", "content": "Content 1", "location": "Location 1", "public_id": "test-public-id-1"},
            {"title": "Review 2", "content": "Content 2", "location": "Location 2", "public_id": "test-public-id-2"},
        ]
        expected_response = {
            "status": "success",
            "message": "Successfully get reviews.",
            "data": expected_data,
        }
        mock_get_all_reviews.return_value = expected_response
        page = 1
        count = 2

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/review?page={page}&count={count}")
            result = json.loads(response.data.decode("utf-8"))
            result = result.get("data")
            first_review = result[0]
            second_review = result[1]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(first_review.get("title"), expected_data[0].get("title"))
        self.assertEqual(first_review.get("content"), expected_data[0].get("content"))
        self.assertEqual(first_review.get("location"), expected_data[0].get("location"))
        self.assertEqual(first_review.get("public_id"), expected_data[0].get("public_id"))
        self.assertEqual(second_review.get("title"), expected_data[1].get("title"))
        self.assertEqual(second_review.get("content"), expected_data[1].get("content"))
        self.assertEqual(
            second_review.get("location"), expected_data[1].get("location")
        )
        self.assertEqual(second_review.get("public_id"), expected_data[1].get("public_id"))
        mock_get_all_reviews.assert_called_once()
    
    @patch("app.main.controller.review_controller.get_all_reviews")
    def test_get_all_reviews_with_filters(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {
                "title": "Review 1", 
                "content": "Content 1", 
                "location": "Location 1", 
                "public_id": "test-public-id-1", 
                "tag_id": "test-tag-id", 
                "category_id": "test-category-id", 
                "region_id": "test-region-id"
            },
            {
                "title": "Review 2", 
                "content": "Content 2", 
                "location": "Location 2", 
                "public_id": "test-public-id-2", 
                "tag_id": "test-tag-id", 
                "category_id": "test-category-id", 
                "region_id": "test-region-id"
            },
            {
                "title": "Review 3",
                "content": "Content 3",
                "location": "Location 3",
                "public_id": "test-public-id-3",
                "tag_id": "test-tag-id",
                "category_id": "test-category-id",
                "region_id": "test-region-id"
            }
        ]
        expected_response = {
            "status": "success",
            "message": "Successfully get reviews.",
            "data": expected_data,
        }
        mock_get_all_reviews.return_value = expected_response
        page = 1
        count = 2
        tag_id = "test-tag-id"
        category_id = "test-category-id"
        region_id = "test-region-id"

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/review?page={page}&count={count}&tag_id={tag_id}&category_id={category_id}&region_id={region_id}")
            result = json.loads(response.data.decode("utf-8"))
            result = result.get("data")
            first_review = result[0]
            second_review = result[1]
            third_review = result[2]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(first_review.get("title"), expected_data[0].get("title"))
        self.assertEqual(first_review.get("content"), expected_data[0].get("content"))
        self.assertEqual(first_review.get("location"), expected_data[0].get("location"))
        self.assertEqual(first_review.get("public_id"), expected_data[0].get("public_id"))
        self.assertEqual(second_review.get("tag_id"), expected_data[1].get("tag_id"))
        self.assertEqual(second_review.get("category_id"), expected_data[1].get("category_id"))
        self.assertEqual(second_review.get("region_id"), expected_data[1].get("region_id"))
        self.assertEqual(second_review.get("title"), expected_data[1].get("title"))
        self.assertEqual(second_review.get("content"), expected_data[1].get("content"))
        self.assertEqual(
            second_review.get("location"), expected_data[1].get("location")
        )
        self.assertEqual(second_review.get("public_id"), expected_data[1].get("public_id"))
        self.assertEqual(third_review.get("tag_id"), expected_data[2].get("tag_id"))
        self.assertEqual(third_review.get("category_id"), expected_data[2].get("category_id"))
        self.assertEqual(third_review.get("region_id"), expected_data[2].get("region_id"))
        mock_get_all_reviews.assert_called_once()

    @patch("app.main.controller.review_controller.get_a_review")
    def test_get_a_review(self, mock_get_a_review):
        # ARRANGE
        public_id = "test-public-id"
        expected_response = {
            "status": "success",
            "message": "Successfully retrieved.",
            "data": review_data,
        }
        mock_get_a_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get(f"/api/review/{public_id}")
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("title"), res["data"].get("title")
        )
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        self.assertEqual(
            expected_response["data"].get("location"), res["data"].get("location")
        )

    @patch("app.main.controller.review_controller.update_review")
    def test_update_review(self, mock_update_review):
        # ARRANGE
        public_id = "test-public-id"
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": review_data,
        }
        mock_update_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/review/{public_id}", json=review_data)
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("title"), res["data"].get("title")
        )
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        self.assertEqual(
            expected_response["data"].get("location"), res["data"].get("location")
        )
        mock_update_review.assert_called_once()

    @patch("app.main.controller.review_controller.delete_review")
    def test_delete_review(self, mock_delete_review):
        # ARRANGE
        public_id = "test-public-id"
        review_data["public_id"] = public_id
        expected_response = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": review_data,
        }
        mock_delete_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.delete(f"/api/review/{public_id}")
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("title"), res["data"].get("title")
        )
        self.assertEqual(
            expected_response["data"].get("content"), res["data"].get("content")
        )
        self.assertEqual(
            expected_response["data"].get("location"), res["data"].get("location")
        )
        mock_delete_review.assert_called_once()

    @patch("app.main.controller.review_controller.upvote_review")
    def test_upvote_review(self, mock_upvote_review):
        # ARRANGE
        public_id = "test-public_id"
        review_data["public_id"] = public_id
        review_data["upvotes"] = 2
        review_data["downvotes"] = 1
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": review_data,
        }
        mock_upvote_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/review/{public_id}/vote", json=review_data)
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("upvotes"), res["data"].get("upvotes")
        )
        self.assertEqual(
            expected_response["data"].get("downvotes"), res["data"].get("downvotes")
        )
        mock_upvote_review.assert_called_once()

    @patch("app.main.controller.review_controller.update_visibility")
    def test_visibility_review(self, mock_visibility_review):
        # ARRANGE
        public_id = "test-public_id"
        review_data["public_id"] = public_id
        review_data["visible"] = False
        expected_response = {
            "status": "success",
            "message": "Successfully updated.",
            "data": review_data,
        }
        mock_visibility_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(f"/api/review/{public_id}/status", json=review_data)
            res = json.loads(response.data.decode("utf-8"))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            expected_response["data"].get("visible"), res["data"].get("visible")
        )
        mock_visibility_review.assert_called_once()
    
    @patch("app.main.controller.review_controller.create_review")
    def test_create_review_missing_title(self, mock_create_review):
        # ARRANGE
        review_data_missing_title = {
            "content": "This is a test review.",
            "location": "Test Location",
            "region_id": "test-region-id",
        }
        expected_response = {
            "message": error_message,
            "errors": {'title': "'title' is a required property"},
        }
        mock_create_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/review", json=review_data_missing_title)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])
    
    @patch("app.main.controller.review_controller.create_review")
    def test_create_review_missing_content(self, mock_create_review):
        # ARRANGE
        review_data_missing_content = {
            "title": "Test Review",
            "location": "Test Location",
            "region_id": "test-region-id",
        }
        expected_response = {
            "message": error_message,
            "errors": {'content': "'content' is a required property"},
        }
        mock_create_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/review", json=review_data_missing_content)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])
    
    @patch("app.main.controller.review_controller.create_review")
    def test_create_review_missing_region_id(self, mock_create_review):
        # ARRANGE
        review_data_missing_region_id = {
            "title": "Test Review",
            "content": "This is a test review.",
            "location": "Test Location",
        }
        expected_response = {
            "message": error_message,
            "errors": {'region_id': "'region_id' is a required property"},
        }
        mock_create_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/review", json=review_data_missing_region_id)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["message"], res["message"])
        self.assertEqual(expected_response["errors"], res["errors"])
        

import os
import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app

os.environ["DEBUG"] = "True"

review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
    "region_id": "test-region-id",
}

error_message = "Input payload validation failed"

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

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/review", json=review_data)
            res = response.get_json()
            res = res.get("data")

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["data"]["title"], res.get("title"))
        self.assertEqual(expected_response["data"]["content"], res.get("content"))
        self.assertEqual(expected_response["data"]["location"], res.get("location"))
        mock_create_review.assert_called_once()

    @patch("app.main.controller.review_controller.get_all_reviews")
    def test_get_all_reviews(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {"title": "Review 1", "content": "Content 1", "location": "Location 1"},
            {"title": "Review 2", "content": "Content 2", "location": "Location 2"},
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
        self.assertEqual(first_review.get("title"), expected_data[0].get("title"))
        self.assertEqual(first_review.get("content"), expected_data[0].get("content"))
        self.assertEqual(first_review.get("location"), expected_data[0].get("location"))
        self.assertEqual(second_review.get("title"), expected_data[1].get("title"))
        self.assertEqual(second_review.get("content"), expected_data[1].get("content"))
        self.assertEqual(
            second_review.get("location"), expected_data[1].get("location")
        )
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
        

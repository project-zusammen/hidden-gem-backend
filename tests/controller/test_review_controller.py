import json
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.extensions import db
from app.main.util.dto import ReviewDto

review_data = {
    'title': 'Test Review',
    'content': 'This is a test review.',
    'location': 'Test Location',
}


class TestReviewEndpoints(TestCase):

    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.main.controller.review_controller.create_review')
    def test_create_review(self, mock_create_review):
        # ARRANGE
        expected_response = {
            'status': 'success',
            'message': 'Successfully created.',
            'data': review_data
        }
        mock_create_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.post('/api/review', json=review_data)
            res = response.get_json()
            res = res.get('data')

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response['data']['title'], res.get('title'))
        self.assertEqual(expected_response['data']['content'], res.get('content'))
        self.assertEqual(expected_response['data']['location'], res.get('location'))
        mock_create_review.assert_called_once()

    @patch('app.main.controller.review_controller.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {"title": "Review 1", "content": "Content 1", "location": "Location 1"},
            {"title": "Review 2", "content": "Content 2", "location": "Location 2"}
        ]
        expected_response = {
            'status': 'success',
            'message': 'Successfully get reviews.',
            'data': expected_data
        }
        mock_get_all_reviews.return_value = expected_response

        # ACT 
        with self.app.test_client() as client:
            response = client.get('/api/review')
            result = json.loads(response.data.decode('utf-8'))
            result = result.get('data')
            first_review = result[0]
            second_review = result[1]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(first_review.get('title'), expected_data[0].get('title'))
        self.assertEqual(first_review.get('content'), expected_data[0].get('content'))
        self.assertEqual(first_review.get('location'), expected_data[0].get('location'))
        self.assertEqual(second_review.get('title'), expected_data[1].get('title'))
        self.assertEqual(second_review.get('content'), expected_data[1].get('content'))
        self.assertEqual(second_review.get('location'), expected_data[1].get('location'))
        mock_get_all_reviews.assert_called_once()

    

    @patch('app.main.controller.review_controller.get_a_review')
    def test_get_a_review(self, mock_get_a_review):
        # ARRANGE
        public_id = 'test-public-id'
        expected_response = {
            'status': 'success',
            'message': 'Successfully retrieved.',
            'data': review_data
        }
        mock_get_a_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.get(f'/api/review/{public_id}')
            res = json.loads(response.data.decode('utf-8'))
        
        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get('title'), res.get('title'))
        self.assertEqual(expected_response.get('content'), res.get('content'))
        self.assertEqual(expected_response.get('location'), res.get('location'))

    @patch('app.main.controller.review_controller.update_review')
    def test_update_review(self, mock_update_review):
        # ARRANGE
        public_id = 'test-public-id'
        expected_response = {
            'status': 'success',
            'message': 'Successfully updated.',
            'data': review_data
        }
        mock_update_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.put(f'/api/review/{public_id}', json=review_data)
            res = json.loads(response.data.decode('utf-8'))

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get('title'), res.get('title'))
        self.assertEqual(expected_response.get('content'), res.get('content'))
        self.assertEqual(expected_response.get('location'), res.get('location'))
        mock_update_review.assert_called_once()

    @patch('app.main.controller.review_controller.delete_review')
    def test_delete_review(self, mock_delete_review):
        # ARRANGE
        public_id = 'test-public-id'
        review_data['public_id'] = public_id 
        expected_response = {
            'status': 'success',
            'message': 'Successfully deleted.',
            'data': review_data
        }
        mock_delete_review.return_value = expected_response

        # ACT
        with self.app.test_client() as client:
            response = client.delete(f'/api/review/{public_id}')
            res = json.loads(response.data.decode('utf-8'))
        
        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response.get('title'), res.get('title'))
        self.assertEqual(expected_response.get('content'), res.get('content'))
        self.assertEqual(expected_response.get('location'), res.get('location'))
        mock_delete_review.assert_called_once()
import unittest
import json
from unittest.mock import patch
from app import create_app
from app.extensions import db
from app.main.util.dto import ReviewDto

review_dto = ReviewDto()
_review = review_dto.review
review_data = {
    'title': 'Test Review',
    'content': 'This is a test review.',
    'location': 'Test Location',
}


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()
        self.app_context.pop()

    @patch('app.main.service.review_service.create_review')
    def test_create_review(self, mock_create_review):
        # ARRANGE
        expected_data = {"title": "Test Review", "content": "Test Content", "location": "Test Location"}
        mock_create_review.return_value = expected_data

        # ACT
        with self.app.test_client() as client:
            response = client.get('/api/review', json=expected_data)
            res = json.loads(response.data.decode('utf-8'))

        # ASSERT
        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected_data.get('title'), res.get('title'))
        self.assertEqual(expected_data.get('content'), res.get('content'))
        self.assertEqual(expected_data.get('location'), res.get('location'))
        mock_create_review.assert_called_once()


    @patch('app.main.service.review_service.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {"title": "Review 1", "content": "Content 1", "location": "Location 1"},
            {"title": "Review 2", "content": "Content 2", "location": "Location 2"}
        ]
        mock_get_all_reviews.return_value = expected_data

        # ACT 
        with self.app.test_client() as client:
            response = client.get('/api/review')
            result = json.loads(response.data.decode('utf-8'))
            print('result', result)
            res = result.get('data')
            print('res', res)
            first_review = res[0]
            second_review = res[1]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(res, list)
        self.assertEqual(first_review.get('title'), expected_data[0].get('title'))
        self.assertEqual(first_review.get('content'), expected_data[0].get('content'))
        self.assertEqual(first_review.get('location'), expected_data[0].get('location'))
        self.assertEqual(second_review.get('title'), expected_data[1].get('title'))
        self.assertEqual(second_review.get('content'), expected_data[1].get('content'))
        self.assertEqual(second_review.get('location'), expected_data[1].get('location'))
        mock_get_all_reviews.assert_called_once()

    

    @patch('app.main.service.review_service.get_a_review')
    def test_get_a_review(self, mock_get_a_review):
        # TODO: Implement test for get_a_review endpoint
        pass

    @patch('app.main.service.review_service.update_review')
    def test_update_review(self, mock_update_review):
        # TODO: Implement test for update_review endpoint
        pass

    @patch('app.main.service.review_service.delete_review')
    def test_delete_review(self, mock_delete_review):
        # TODO: Implement test for delete_review endpoint
        pass

if __name__ == '__main__':
    unittest.main()
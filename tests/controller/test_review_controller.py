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

        with self.app.app_context():
            db.create_all()

            
            response = self.client.post('/api/review', json=review_data)
            self.assertEqual(response.status_code, 201)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.main.service.review_service.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all_reviews):
        # ARRANGE
        expected_data = [
            {"public_id": "1", "title": "Review 1", "content": "Content 1"},
            {"public_id": "2", "title": "Review 2", "content": "Content 2"}
        ]
        mock_get_all_reviews.return_value = expected_data

        # ACT 
        response = self.client.get('/api/review')
        print('response.data: ', response.data)
        data = json.loads(response.data.decode('utf-8'))
       
        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(data, expected_data)
        mock_get_all_reviews.assert_called_once()

    @patch('app.main.service.review_service.create_review')
    def test_create_review(self, mock_create_review):
        # TODO: Implement test for create_review endpoint
        pass

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

import uuid
from unittest import TestCase, mock
from unittest.mock import MagicMock
from app import create_app
from app.extensions import db
from app.main.service.review_service import (
    create_review,
    update_review,
    upvote_review,
    update_visibility,
    get_all_reviews,
    get_a_review,
    delete_review
)

def generate_fake_public_id():
    return str(uuid.uuid4())

class TestReviewService(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="app.test_settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    # def test_get_all_reviews(self):
    #     # Arrange
    #     data = [
    #         {"public_id": "fake_id_1", "title": "Test Review 1", "content": "Content 1", "location": "Location 1"},
    #         {"public_id": "fake_id_2", "title": "Test Review 2", "content": "Content 2", "location": "Location 2"}
    #     ]
    #     with mock.patch('app.main.model.review.review_model.get_all_reviews') as mock_get_all_reviews:
    #         mock_get_all_reviews.return_value  = [
    #             MagicMock(serialize=lambda: data[0]),
    #             MagicMock(serialize=lambda: data[1])
    #         ]

    #     # Act
    #     response, status_code = get_all_reviews()
    #     print('response nih', response)
    #     result = response['data']

    #     # Assert
    #     self.assertEqual(status_code, 200)
    #     self.assertEqual(response['status'], 'success')
    #     self.assertEqual(response['message'], 'Successfully retrieved reviews.')
    #     self.assertEqual(len(result), len(data))

    #     mock_review_model.get_all_reviews.assert_called_once()

    #     for i in range(len(result)):
    #         self.assertEqual(result[i]['public_id'], data[i]['public_id'])
    #         self.assertEqual(result[i]['title'], data[i]['title'])
    #         self.assertEqual(result[i]['content'], data[i]['content'])
    #         self.assertEqual(result[i]['location'], data[i]['location'])

    def test_create_review(self):
        # Arrange
        data = {"title": "Test Review", "content": "This is a content review", "location": "Test Location"}
        with mock.patch('app.main.model.review.review_model.create_review') as mock_create_review:
            mock_create_review.return_value = data

        # Act
        response, status_code = create_review(data)
        result = response['data']

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['message'], 'Successfully created.')
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['content'], data['content'])
        self.assertEqual(result['location'], data['location'])
    
    # @patch('app.main.model.review.review_model')
    # def test_update_review(self, mock_review_model):
        # Arrange
        # fake_public_id = generate_fake_public_id()
        # data = {"title": "Test Review updated", "content": "This is a content review updated", "location": "Test Location updated"}
        # data['public_id'] = fake_public_id
        # mock_review_model.update_review.return_value = data

        # # Act
        # response, status_code = update_review(fake_public_id, data)
        # print('response', response)
        # result = response['data']

        # # Assert
        # self.assertEqual(status_code, 201)
        # self.assertEqual(response['status'], 'success')
        # self.assertEqual(response['message'], 'Successfully updated.')
        # self.assertEqual(result['title'], data['title'])
        # self.assertEqual(result['content'], data['content'])
        # self.assertEqual(result['location'], data['location'])

    # Similar tests for other functions...

if __name__ == '__main__':
    unittest.main()

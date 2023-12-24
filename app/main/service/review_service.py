import uuid
import datetime

from app.main.model.review import Review
from ..model import get_all

def create_review(data):
    review = Review(
        public_id=str(uuid.uuid4()),
        # category_id = data.get('category_id'),
        # region_id = data.get('region_id'),
        title = data.get('title'),
        content = data.get('content'),
        location = data.get('location'),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    review.save()
    response_object = {
        'status': 'success',
        'message': 'Successfully created.',
        'data': review.serialize()
    }
    return response_object, 201


def update_review(public_id, data):
    review = Review.query.filter_by(public_id=public_id).first()
    if not review:
        response_object = {
            'status': 'fail',
            'message': 'Review does not exist.'
        }
        return response_object, 409
    else:
        review.category_id = data.get('category_id')
        review.region_id = data.get('region_id')
        review.title = data.get('title')
        review.content = data.get('content')
        review.location = data.get('location')
        review.updated_at = datetime.datetime.utcnow()
        review.save()
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.',
            'data': review.serialize()
        }
        return response_object, 201


def upvote_review(public_id, upvote=True):
    review = Review.query.filter_by(public_id=public_id).first()
    if not review:
        response_object = {
            'status': 'fail',
            'message': 'Review does not exist.'
        }
        return response_object, 409
    else:
        if upvote:
            review.upvotes += 1
        else:
            review.downvotes += 1
        review.save()
        response_object = {
            'status': 'success',
            'message': 'Successfully upvoted.',
            'data': review.serialize()
        }
        return response_object, 201


def update_visibility(public_id, visible=True):
    review = Review.query.filter_by(public_id=public_id).first()
    if not review:
        response_object = {
            'status': 'fail',
            'message': 'Review does not exist.'
        }
        return response_object, 409
    else:
        review.visible = visible
        review.save()
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.',
            'data': review.serialize()
        }
        return response_object, 201


def get_all_reviews():
    try:
        reviews = get_all()
        if not reviews:
            return {'status': 'success', 'message': 'No reviews found', 'data': []}, 200

        review_data = [review.serialize() for review in reviews]

        response_object = {
            'status': 'success',
            'message': 'Successfully retrieved reviews.',
            'data': review_data
        }
        return response_object, 200
    except Exception as e:
        print(f"Error in get_all_reviews: {str(e)}")
        return {'status': 'error', 'message': 'Internal Server Error'}, 500



def get_a_review(public_id):
    review = Review.query.filter_by(public_id=public_id).first()
    if not review:
        response_object = {
            'status': 'fail',
            'message': 'Review does not exist.'
        }
        return response_object, 409
    
    response_object = {
        'status': 'success',
        'message': 'Successfully get a review.',
        'data': review.serialize()
    }
    return response_object, 200


def delete_review(public_id):
    review = Review.query.filter_by(public_id=public_id).first()
    if not review:
        response_object = {
            'status': 'fail',
            'message': 'Review does not exist.'
        }
        return response_object, 409
    else:
        review.visible = False
        review.save()
        review = Review.query.filter_by(public_id=public_id).first()
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
            'data': review.serialize()
        }
        return response_object, 201



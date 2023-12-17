import uuid
import datetime

from app.main import db
from app.main.model.review import Review


def create_review(data):
    review = Review(
        public_id=str(uuid.uuid4()),
        category_id = data.get('category_id'),
        region_id = data.get('region_id'),
        title = data.get('title'),
        content = data.get('content'),
        location = data.get('location'),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
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
    reviews = Review.query.filter_by(visible=True).all()
    response_object = {
        'status': 'success',
        'message': 'Successfully get reviews.',
        'data': [review.to_json() for review in reviews]
    }
    return response_object, 200


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
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
            'data': review.serialize()
        }
        return response_object, 201



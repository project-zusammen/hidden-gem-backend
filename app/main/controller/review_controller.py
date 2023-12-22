from flask import request
from flask_restx import Resource

from ..util.dto import ReviewDto
from ..service.review_service import create_review, get_all_reviews, get_a_review

api = ReviewDto.api
_review = ReviewDto.review


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_of_reviews')
    @api.marshal_list_with(_review, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_reviews()

    @api.response(201, 'Review successfully created.')
    @api.doc('create a new review')
    @api.expect(_review, validate=True)
    def post(self):
        """Creates a new Review """
        data = request.json
        return create_review(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Review identifier')
@api.response(404, 'Review not found.')
class Review(Resource):
    @api.doc('get a review')
    @api.marshal_with(_review)
    def get(self, public_id):
        """get a review given its identifier"""
        review = get_a_review(public_id)
        if not review:
            api.abort(404)
        else:
            return review
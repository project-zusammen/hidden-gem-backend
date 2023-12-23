from flask import Blueprint, request
from flask_restx import Api, Resource

from ..util.dto import ReviewDto
from ..service.review_service import create_review, get_all_reviews, get_a_review

# Import the ReviewDto
review_dto = ReviewDto()

# Create a Blueprint and Api
review_bp = Blueprint('review', __name__)
api = Api(review_bp)

@api.route('/')
class ReviewList(Resource):
    # @api.doc('list_of_reviews')
    def get(self):
        """List all reviews"""
        return get_all_reviews()

    @api.doc('create a new review')
    # @api.expect(_review, validate=True)
    def post(self):
        """Creates a new Review"""
        data = request.json
        return create_review(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Review identifier')
@api.response(404, 'Review not found.')
class Review(Resource):
    @api.doc('get a review')
    def get(self, public_id):
        """Get a review by its identifier"""
        review = get_a_review(public_id)
        return review

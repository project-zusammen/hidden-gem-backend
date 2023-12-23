from ..util.dto import ReviewDto

review_dto = ReviewDto()
_review = review_dto.review

from flask_restx import Resource
from ..service.review_service import create_review, get_all_reviews, get_a_review, update_review, delete_review
from ...extensions import ns

@ns.route('/review')
class ReviewList(Resource):
    def get(self):
        """List all reviews"""
        return get_all_reviews()

    @ns.expect(_review, validate=True)
    def post(self):
        """Creates a new Review"""
        return create_review(ns.payload)


@ns.route('/review/<public_id>')
@ns.param('public_id', 'The Review identifier')
class Review(Resource):
    def get(self, public_id):
        """Get a review by its identifier"""
        review = get_a_review(public_id)
        return review
    
    @ns.expect(_review, validate=True)
    def put(self, public_id):
        """Update a review"""
        updated_review = update_review(public_id, ns.payload)
        return updated_review
    
    def delete(self, public_id):
        """Delete a review"""
        return delete_review(public_id)
    
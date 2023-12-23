from ..util.dto import ReviewDto

review_dto = ReviewDto()

from flask_restx import Resource
from ..service.review_service import create_review, get_all_reviews, get_a_review
from ...extensions import ns, api

@ns.route('/review')
class ReviewList(Resource):
    def get(self):
        """List all reviews"""
        return get_all_reviews()

    @ns.expect(review_dto, validate=True)
    def post(self):
        """Creates a new Review"""
        data = api.payload
        return create_review(data=data)


@ns.route('/review/<public_id>')
@ns.param('public_id', 'The Review identifier')
class Review(Resource):
    def get(self, public_id):
        """Get a review by its identifier"""
        review = get_a_review(public_id)
        return review
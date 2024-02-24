from ..util.dto import ReviewDto

review_dto = ReviewDto()
_review = review_dto.review
_upvote = review_dto.upvote
_visible = review_dto.visible

from flask_restx import Resource
from ..service.review_service import (
    create_review,
    get_all_reviews,
    get_a_review,
    update_review,
    delete_review,
    upvote_review,
    update_visibility,
)
from ...extensions import ns


@ns.route("/review")
class ReviewList(Resource):
    @ns.cache.cached(timeout = 300)
    def get(self):
        """List all reviews"""
        return get_all_reviews()

    @ns.expect(_review, validate=True)
    def post(self):
        """Creates a new Review"""
        return create_review(ns.payload)


@ns.route("/review/<public_id>")
@ns.param("public_id", "The Review identifier")
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


@ns.route("/review/<public_id>/vote")
@ns.param("public_id", "The Review Identifier")
class ReviewUpvote(Resource):
    @ns.expect(_upvote)
    def put(self, public_id):
        """Give upvote or downvote"""
        upvote = ns.payload.get("upvote")
        upvoted_review = upvote_review(public_id, upvote)
        return upvoted_review


@ns.route("/review/<public_id>/status")
@ns.param("public_id", "The Review Identifier")
class ReviewVisible(Resource):
    @ns.expect(_visible)
    def put(self, public_id):
        """Update visibility status"""
        visible = ns.payload.get("visible")
        updated_visibility = update_visibility(public_id, visible)
        return updated_visibility

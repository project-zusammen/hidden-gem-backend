from flask_restx import Resource, Namespace
from ...extensions import authorizations
from ..util.dto import ReviewDto
from flask import request
from ..util.dto import ReviewDto
from ..util.token_verify import token_required

review_dto = ReviewDto()
_review = review_dto.review
_upvote = review_dto.upvote
_visible = review_dto.visible

from ..service.review_service import (
    create_review,
    get_all_reviews,
    get_a_review,
    update_review,
    delete_review,
    upvote_review,
    update_visibility,
)

ns = Namespace("review", authorizations=authorizations)

review_dto = ReviewDto()
_review = review_dto.review
_upvote = review_dto.upvote
_visible = review_dto.visible


@ns.route("")
class ReviewList(Resource):
    @ns.param("page", "Page of data you want to retrieve")
    @ns.param("count", "How many items you want to include in each page")
    @ns.param("tag_id", "Retrieve data based on the specified tag")
    @ns.param("category_id", "Retrieve data based on the specified category")
    @ns.param("region_id", "Retrieve data based on the specified region")
    def get(self):
        """List all reviews"""
        page = request.args.get("page", default=1, type=int)
        count = request.args.get("count", default=50, type=int)
        tag_id = request.args.get("tag_id", default="", type=str)
        category_id = request.args.get("category_id", default="", type=str)
        region_id = request.args.get("region_id", default="", type=str)
        return get_all_reviews(page, count, tag_id, category_id, region_id)

    @ns.expect(_review, validate=True)
    @ns.doc(security="bearer")
    @token_required
    def post(self, decoded_token):
        """Creates a new Review"""
        user_id = decoded_token["id"]
        return create_review(ns.payload, user_id)


@ns.route("/<public_id>")
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


@ns.route("/<public_id>/vote")
@ns.param("public_id", "The Review Identifier")
class ReviewUpvote(Resource):
    @ns.expect(_upvote)
    def put(self, public_id):
        """Give upvote or downvote"""
        upvote = ns.payload.get("upvote")
        upvoted_review = upvote_review(public_id, upvote)
        return upvoted_review


@ns.route("/<public_id>/status")
@ns.param("public_id", "The Review Identifier")
class ReviewVisible(Resource):
    @ns.expect(_visible)
    def put(self, public_id):
        """Update visibility status"""
        visible = ns.payload.get("visible")
        updated_visibility = update_visibility(public_id, visible)
        return updated_visibility

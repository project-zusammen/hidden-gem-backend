from ..util.dto import CommentDto
from ..util.token_verify import token_required
from ..util.helper import error_handler
from flask import request

comment_dto = CommentDto()
_comment = comment_dto.comment
_upvote = comment_dto.upvote
_visible = comment_dto.visible

from flask_restx import Resource
from ..service.comment_service import (
    get_all_comments,
    create_comment,
    get_a_comment,
    delete_comment,
    update_comment,
    upvote_comment,
    update_visibility,
)
from ...extensions import ns


@ns.route("/comment")
class CommentList(Resource):
    @ns.param("page", "Which page number you want to query?")
    @ns.param("count", "How many items you want to include in each page?")
    def get(self):
        """List all comment"""
        page = request.args.get("page", default=1, type=int)
        count = request.args.get("count", default=10, type=int)
        return get_all_comments(page, count)

    @ns.expect(_comment, validate=True)
    def post(self):
        """Create a new comment"""
        return create_comment(ns.payload)


@ns.route("/comment/<public_id>")
@ns.param("public_id", "The comment identifier")
class Comment(Resource):
    def get(self, public_id):
        """Get a comment by its identifier"""
        comment = get_a_comment(public_id)
        return comment

    def delete(self, public_id):
        """Delete a comment"""
        return delete_comment(public_id)

    @ns.expect(_comment, validate=True)
    def put(self, public_id):
        """Update a comment"""
        updated_comment = update_comment(public_id, ns.payload)

        return updated_comment


@ns.route("/comment/<public_id>/vote")
@ns.param("public_id", "The Comment Identifier")
class CommentUpvote(Resource):
    @ns.expect(_upvote)
    def put(self, public_id):
        """Give upvote or downvote"""
        upvote = ns.payload.get("upvote")
        upvoted_comment = upvote_comment(public_id, upvote)
        return upvoted_comment


@ns.route("/comment/<public_id>/status")
@ns.param("public_id", "The Comment Identifier")
class CommentVisible(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_visible)
    def put(self, decoded_token, public_id):
        """Update visibility status"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        visible = ns.payload.get("visible")
        updated_visibility = update_visibility(public_id, visible)
        return updated_visibility

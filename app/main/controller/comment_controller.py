from flask_restx import Resource, Namespace

from ...extensions import authorizations
from ..util.dto import CommentDto
from ..service.comment_service import (
    get_all_comments,
    create_comment,
    get_a_comment,
    delete_comment,
    update_comment,
    upvote_comment,
    update_visibility,
)

ns = Namespace("api/comment", authorizations=authorizations)

comment_dto = CommentDto()
_comment = comment_dto.comment
_upvote = comment_dto.upvote
_visible = comment_dto.visible


@ns.route("/")
class CommentList(Resource):
    def get(self):
        """List all comment"""
        return get_all_comments()

    @ns.expect(_comment, validate=True)
    def post(self):
        """Create a new comment"""
        return create_comment(ns.payload)


@ns.route("/<public_id>")
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


@ns.route("/<public_id>/vote")
@ns.param("public_id", "The Comment Identifier")
class CommentUpvote(Resource):
    @ns.expect(_upvote)
    def put(self, public_id):
        """Give upvote or downvote"""
        upvote = ns.payload.get("upvote")
        upvoted_comment = upvote_comment(public_id, upvote)
        return upvoted_comment


@ns.route("/<public_id>/status")
@ns.param("public_id", "The Comment Identifier")
class CommentVisible(Resource):
    @ns.expect(_visible)
    def put(self, public_id):
        """Update visibility status"""
        visible = ns.payload.get("visible")
        updated_visibility = update_visibility(public_id, visible)
        return updated_visibility

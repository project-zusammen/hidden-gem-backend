from ..util.dto import CommentDto

comment_dto = CommentDto()
_comment = comment_dto.comment

from flask_restx import Resource
from ..service.comment_service import get_all_comments, create_comment
from ...extensions import ns

@ns.route('/comments')
class CommentList(Resource):
    def get(self):
        """List all comment"""
        return get_all_comments()

    @ns.expect(_comment, validate=True)
    def post(self):
        """Creates a new Review"""
        return create_comment(ns.payload)
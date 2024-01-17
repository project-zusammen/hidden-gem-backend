from ..util.dto import CommentDto

comment_dto = CommentDto()
_comment = comment_dto.comment

from flask_restx import Resource
from ..service.comment_service import (
    get_all_comments, 
    create_comment, 
    delete_comment
)
from ...extensions import ns

@ns.route('/comment')
class CommentList(Resource):
    def get(self):
        """List all comment"""
        return get_all_comments()
    
    @ns.expect(_comment, validate=True)
    def post(self):
        """Create a new comment"""
        return create_comment(ns.payload)
    
@ns.route("/comment/<public_id>")
@ns.param("public_id", "The comment identifier")
class Comment(Resource):
    def delete(self, public_id):
        """Delete a comment"""
        return delete_comment(public_id)
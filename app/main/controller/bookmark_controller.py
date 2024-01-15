from ..util.dto import BookmarkDto

bookmark_dto = BookmarkDto()
_bookmark =bookmark_dto.bookmark

from flask_restx import Resource
from ..service.bookmark_service import (
    create_bookmark,
    get_bookmark_by_userid,
    delete_bookmark
)
from ...extensions import ns

@ns.route("/bookmark")
class CreateBookmark(Resource):
    @ns.expect(_bookmark, validate=True)
    def post(self):
        """Register a new bookmark"""
        return create_bookmark(ns.payload)

## it should be in /bookmark routes after the authentication is applied
@ns.route("/bookmark/<user_id>")
@ns.param("user_id", "The user identifier")
class Bookmark(Resource):
    def get(self, user_id):
        """Get a bookmark list own by user"""
        bookmark = get_bookmark_by_userid(user_id)
        return bookmark

@ns.route("/bookmark/<public_id>")
@ns.param("public_id", "The bookmark identifier")
class DeleteBookmark(Resource):
    def delete(self, public_id):
        """Delete review from bookmarks"""
        deleted_bookmark = delete_bookmark(public_id)
        return deleted_bookmark
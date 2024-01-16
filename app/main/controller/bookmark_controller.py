from ..util.dto import BookmarkDto

bookmark_dto = BookmarkDto()
_bookmark = bookmark_dto.bookmark

from flask_restx import Resource
from ..service.bookmark_service import (
    create_bookmark,
    get_bookmark_by_userid,
    delete_bookmark,
)
from ...extensions import ns
from ..util.token_verify import token_required


@ns.route("/bookmark")
class CreateBookmark(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_bookmark, validate=True)
    def post(self, decoded_token):
        """Add review to user bookmark"""
        return create_bookmark(ns.payload)

    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """Get a list of bookmarks owned by the authenticated user."""
        user_public_id = decoded_token["public_id"]
        return get_bookmark_by_userid(user_public_id)


@ns.route("/bookmark/<public_id>")
@ns.param("public_id", "The bookmark identifier")
class DeleteBookmark(Resource):
    @ns.doc(security="bearer")
    @token_required
    def delete(self, decoded_token, public_id):
        """Delete review from bookmarks"""
        user_id = decoded_token["id"]
        return delete_bookmark(public_id, user_id)

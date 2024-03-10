from ..util.dto import BookmarkDto
from flask_restx import Resource, Namespace
from ...extensions import authorizations
from ..service.bookmark_service import (
    create_bookmark,
    get_bookmark_by_userid,
    delete_bookmark,
)
from ..util.token_verify import token_required

bookmark_dto = BookmarkDto()
_bookmark = bookmark_dto.bookmark

ns = Namespace("bookmark", authorizations=authorizations)

@ns.route("/bookmark")
class CreateBookmark(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_bookmark, validate=True)
    def post(self, decoded_token):
        """Add review to user bookmark"""
        user_id = decoded_token["id"]
        return create_bookmark(ns.payload, user_id)

    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """Get a list of bookmarks owned by the authenticated user."""
        user_id = decoded_token["id"]
        return get_bookmark_by_userid(user_id)


@ns.route("/bookmark/<public_id>")
@ns.param("public_id", "The bookmark identifier")
class DeleteBookmark(Resource):
    @ns.doc(security="bearer")
    @token_required
    def delete(self, decoded_token, public_id):
        """Delete review from bookmarks"""
        user_id = decoded_token["id"]
        return delete_bookmark(public_id, user_id)

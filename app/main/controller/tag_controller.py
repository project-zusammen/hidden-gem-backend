from ..util.dto import TagDto
from ..util.token_verify import token_required

tag_dto = TagDto()
_tag = tag_dto.tag

from flask_restx import Resource
from ..service.tag_service import (
    create_tag,
)

from ...extensions import ns


@ns.route("/tag")
class Tag(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_tag, validate=True)
    def post(self, decoded_token):
        """Create a new tag"""
        return create_tag(ns.payload)



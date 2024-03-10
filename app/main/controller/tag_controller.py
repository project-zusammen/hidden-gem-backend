from ..util.dto import TagDto
from ..util.token_verify import token_required
from ...extensions import authorizations
from flask_restx import Resource, Namespace
from ..service.tag_service import (
    create_tag,
    get_all_tags,
)

tag_dto = TagDto()
_tag = tag_dto.tag

ns = Namespace("tag", authorizations=authorizations)

@ns.route("")
class Tag(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_tag, validate=True)
    def post(self, decoded_token):
        """Create a new tag"""
        return create_tag(ns.payload)
    
    def get(self):
        """List all tags"""
        return get_all_tags()



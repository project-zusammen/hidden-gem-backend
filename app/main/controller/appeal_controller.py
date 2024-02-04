from ..util.dto import AppealDto
from ..util.token_verify import token_required
from ..util.helper import error_handler


from flask_restx import Resource
from ..service.appeal_service import (
    create_appeal,
    get_all_appeals,
    get_a_appeal
)
from ...extensions import ns


appeal_dto = AppealDto()
_appeal = appeal_dto.appeal


@ns.route("/appeal")
class AppealList(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")
        
        """List all appeals"""
        return get_all_appeals()
    
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_appeal, validate=True)
    def post(self, decoded_token):
        """Creates a new appeal"""
        user_id = decoded_token["id"]
        return create_appeal(ns.payload, user_id)
    

@ns.route("/appeal/<public_id>")
@ns.param("public_id", "The appeal identifier")
class Appeal(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token, public_id):
        user_id = decoded_token["id"]
        role = decoded_token["role"]
        """Get a appeal by its identifier"""
        return get_a_appeal(public_id, user_id, role)
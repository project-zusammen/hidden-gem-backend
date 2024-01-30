from ..util.dto import AppealDto

appeal_dto = AppealDto()
_appeal = appeal_dto.appeal

from flask_restx import Resource
from ..service.appeal_service import create_appeal
from ...extensions import ns
from ..util.token_verify import token_required
from ..util.helper import error_handler


@ns.route("/appeal")
class AppealList(Resource):
    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_appeal, validate=True)
    def post(self, decoded_token):
        role = decoded_token["role"]
        if role != "user":
            return error_handler("Access denied")
        
        """Creates a new appeal"""
        return create_appeal(ns.payload)

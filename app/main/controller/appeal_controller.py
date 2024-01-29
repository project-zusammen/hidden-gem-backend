from ..util.dto import AppealDto

appeal_dto = AppealDto()
_appeal = appeal_dto.appeal

from flask_restx import Resource
from ..service.appeal_service import (
    create_appeal,
    get_all_appeals
)
from ...extensions import ns


@ns.route("/appeal")
class AppealList(Resource):
    def get(self):
        """List all appeals"""
        return get_all_appeals()
    
    @ns.expect(_appeal, validate=True)
    def post(self):
        """Creates a new appeal"""
        return create_appeal(ns.payload)

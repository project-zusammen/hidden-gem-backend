from ..util.dto import AppealDto

appeal_dto = AppealDto()
_appeal = appeal_dto.appeal

from flask_restx import Resource
from ..service.appeal_service import create_appeal
from ...extensions import ns


@ns.route("/appeal")
class AppealList(Resource):
    @ns.expect(_appeal, validate=True)
    def post(self):
        """Creates a new appeal"""
        return create_appeal(ns.payload)

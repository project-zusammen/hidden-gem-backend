from ..util.dto import ReportDto
from flask_restx import Resource
from ...extensions import ns
from ..service.report_service import create_report
from ..util.token_verify import token_required

report_dto = ReportDto()
_report = report_dto.report

@ns.route("/report")
class ReportList(Resource):
    @ns.expect(_report, validate=True)
    @ns.doc(security="bearer")
    @token_required
    def post(self, decoded_token):
        """Creates a new Report"""
        user_id = decoded_token["id"]
        return create_report(ns.payload, user_id)
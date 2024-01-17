from ..util.dto import ReportDto
from flask_restx import Resource
from ...extensions import ns
from ..service.report_service import create_report

report_dto = ReportDto()
_report = report_dto.report

@ns.route("/report")
class ReportList(Resource):
    @ns.expect(_report, validate=True)
    def post(self):
        """Creates a new Report"""
        return create_report(ns.payload)
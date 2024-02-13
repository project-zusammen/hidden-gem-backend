from ..util.dto import ReportDto
from flask_restx import Resource
from ...extensions import ns
from ..service.report_service import (
    create_report,
    get_all_reports,
    get_a_report,
    update_report,
)
from ..util.token_verify import token_required
from ..util.helper import error_handler

report_dto = ReportDto()
_report = report_dto.report
_status = report_dto.status


@ns.route("/report")
class ReportList(Resource):
    @ns.expect(_report, validate=True)
    @ns.doc(security="bearer")
    @token_required
    def post(self, decoded_token):
        """Creates a new Report"""
        user_id = decoded_token["id"]
        return create_report(ns.payload, user_id)

    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        """List all reports"""
        return get_all_reports()


@ns.route("/report/<public_id>")
@ns.param("public_id", "The report identifier")
class Report(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token, public_id):
        user_id = decoded_token["id"]
        role = decoded_token["role"]
        """Get a report by its identifier"""
        return get_a_report(public_id, user_id, role)

    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_status)
    def put(self, decoded_token, public_id):
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        """Update report status"""
        status = ns.payload.get("status")
        return update_report(public_id, status)

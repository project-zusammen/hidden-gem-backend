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
from flask import request

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

    @ns.param("page", "Which page number you want to query?")
    @ns.param("count", "How many items you want to include in each page?")
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """List all reports"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        page = request.args.get("page", default=1, type=int)
        count = request.args.get("count", default=20, type=int)
        """List all reports"""
        return get_all_reports(page, count)


@ns.route("/report/<public_id>")
@ns.param("public_id", "The report identifier")
class Report(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token, public_id):
        """Get a report by its identifier"""
        user_id = decoded_token["id"]
        role = decoded_token["role"]
        return get_a_report(public_id, user_id, role)

    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_status)
    def put(self, decoded_token, public_id):
        """Update report status"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        status = ns.payload.get("status")
        return update_report(public_id, status)

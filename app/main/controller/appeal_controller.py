from flask_restx import Resource, Namespace
from ...extensions import authorizations
from ..util.dto import AppealDto
from ..util.token_verify import token_required
from ..util.helper import error_handler
from flask import request

from ..service.appeal_service import (
    create_appeal,
    get_all_appeals,
    get_an_appeal,
    update_appeal,
)

ns = Namespace("appeal", authorizations=authorizations)

appeal_dto = AppealDto()
_appeal = appeal_dto.appeal
_status = appeal_dto.status


@ns.route("/")
class AppealList(Resource):
    @ns.param("page", "Which page number you want to query?")
    @ns.param("count", "How many items you want to include in each page?")
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """List all appeals"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        page = request.args.get("page", default=1, type=int)
        count = request.args.get("count", default=20, type=int)
        return get_all_appeals(page, count)

    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_appeal, validate=True)
    def post(self, decoded_token):
        """Creates a new appeal"""
        user_id = decoded_token["id"]
        return create_appeal(ns.payload, user_id)


@ns.route("/<public_id>")
@ns.param("public_id", "The appeal identifier")
class Appeal(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token, public_id):
        """Get a appeal by its identifier"""
        user_id = decoded_token["id"]
        role = decoded_token["role"]
        return get_an_appeal(public_id, user_id, role)

    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_status)
    def put(self, decoded_token, public_id):
        """Update appeal status"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        status = ns.payload.get("status")
        return update_appeal(public_id, status)

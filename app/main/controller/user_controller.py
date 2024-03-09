from ..util.dto import UserDto
from ..util.helper import error_handler
from flask import request
from flask_restx import Resource
from ..service.user_service import (
    register_user,
    get_all_users,
    get_a_user,
    update_user,
    update_user_status,
    delete_user,
    user_auth,
)
from ...extensions import ns
from ..util.token_verify import token_required

user_dto = UserDto()
_user = user_dto.user
_login = user_dto.login
_userStatus = user_dto.status

@ns.route("/user/signup")
class UserSignUp(Resource):
    @ns.expect(_user, validate=True)
    def post(self):
        """Register a new user"""
        return register_user(ns.payload)


@ns.route("/user")
class UserList(Resource):
    @ns.param("page", "Page of data you want to retrieve")
    @ns.param("count", "How many items you want to include in each page")
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """List all users"""
        page = request.args.get('page', default=1, type=int)
        count = request.args.get('count', default=50, type=int)
        return get_all_users(page, count)


@ns.route("/user/<public_id>")
@ns.param("public_id", "The user identifier")
class User(Resource):
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token, public_id):
        """Get a user by its identifier"""
        user_id = decoded_token["id"]
        return get_a_user(public_id, user_id)

    @ns.doc(security="bearer")
    @token_required
    @ns.expect(_user, validate=True)
    def put(self, decoded_token, public_id):
        """Update a user"""
        user_id = decoded_token["id"]
        updated_user = update_user(public_id, ns.payload, user_id)
        return updated_user

    @ns.doc(security="bearer")
    @token_required
    def delete(self, decoded_token, public_id):
        """Delete a user"""
        user_id = decoded_token["id"]
        return delete_user(public_id, user_id)


## work in progress, need authentication for this endpoint
@ns.route("/user/<public_id>/status")
@ns.param("public_id", "The user identifier")
class UserStatus(Resource):
    @ns.doc(security="bearer")
    @ns.expect(_userStatus, validate=True)
    @token_required
    def put(self, decoded_token, public_id):
        """Update user status"""
        role = decoded_token["role"]
        if role != "admin":
            return error_handler("Access denied")

        updated_user = update_user_status(public_id, ns.payload)
        return updated_user


@ns.route("/user/login")
class UserLogin(Resource):
    @ns.expect(_login, validate=True)
    def post(self):
        """User Authentication"""
        return user_auth(ns.payload)

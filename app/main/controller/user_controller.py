from ..util.dto import UserDto

user_dto = UserDto()

_user = user_dto.user
_login = user_dto.login
_userStatus = user_dto.status
_login = user_dto.login

from flask_restx import Resource
from ..service.user_service import (
    register_user,
    get_all_users,
    get_a_user,
    update_user,
    update_user_status,
    delete_user,
    user_auth
)
from ...extensions import ns
from ..util.token_verify import token_required

@ns.route("/user/signup")
class UserSignUp(Resource):
    @ns.expect(_user, validate=True)
    def post(self):
        """Register a new user"""
        return register_user(ns.payload)
    
@ns.route("/user")
class UserList(Resource):
    def get(self):
        """List all users"""
        return get_all_users()

# example of an endpoint that required a token or login first
@ns.route("/user/<public_id>")
@ns.param("public_id", "The user identifier")
# @token_required
class User(Resource):
    @ns.doc(security='bearer')
    @token_required
    def get(self, decoded_token, public_id):
        """Get a user by its identifier"""
        return get_a_user(public_id)

    @ns.expect(_user, validate=True)
    def put(self, public_id):
        """Update a user"""
        updated_user = update_user(public_id, ns.payload)
        return updated_user

    def delete(self, public_id):
        """Delete a user"""
        return delete_user(public_id)

## work in progress, need authentication for this endpoint
@ns.route("/user/<public_id>/status")
@ns.param("public_id", "The user identifier")
class UserStatus(Resource):
    @ns.doc(security='bearer')
    @ns.expect(_userStatus, validate=True)
    @token_required
    def put(self, decoded_token, public_id):
        role = decoded_token['role']
        if role != "admin":
            return {
                "result" : "error",
                "message": "Access denied: You are not authorized for this operation"
            }
        """Update user status to inactive"""
        updated_user = updated_user_status(public_id, ns.payload)
        return updated_user
    
@ns.route("/user/login")
class UserLogin(Resource):
    @ns.expect(_login, validate=True)
    def post(self):
        """User Authentication"""
        return user_auth(ns.payload)
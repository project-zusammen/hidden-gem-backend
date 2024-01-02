from ..util.dto import UserDto

user_dto = UserDto()
_user = user_dto.user

from flask_restx import Resource
from ..service.user_service import (
    register_user,
    get_all_users,
    get_a_user,
    # update_user,
    delete_user,
)
from ...extensions import ns

@ns.route("/signup")
class UserList(Resource):
    @ns.expect(_user, validate=True)
    def post(self):
        """Register a new user"""
        return register_user(ns.payload)
    
@ns.route("/user")
class UserList(Resource):
    def get(self):
        """List all users"""
        return get_all_users()

@ns.route("/user/<public_id>")
@ns.param("public_id", "The user identifier")
class User(Resource):
    def get(self, public_id):
        """Get a user by its identifier"""
        user = get_a_user(public_id)
        return user

#     @ns.expect(_user, validate=True)
#     def put(self, public_id):
#         """Update a user"""
#         _updateduser = update_user(public_id, ns.payload)
#         return _updateduser

    def delete(self, public_id):
        """Delete a user"""
        return delete_user(public_id)

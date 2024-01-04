import logging as log
from app.main.model.user import User
from ..util.helper import error_handler
log.basicConfig(level=log.ERROR) 

user_model = User()

def register_user(data):
    try:
        result = user_model.register_user(data)  
        response_object = {
            "status": "success",
            "message": "Register User Success.",
            "data": result,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in register_user: {str(e)}")
        return error_handler(e)


def updated_user(public_id, data):
    try:
        updated_user = user_model.update_user(public_id, data)
        response_object = {
            "status": "success",
            "message": "Successfully update user",
            "data": updated_user,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_user: {str(e)}")
        return error_handler(e)

def update_user_status(public_id, data):
    try:
        updated_user = user_model.update_user_status(public_id, data)
        response_object = {
            "status": "success",
            "message": "Successfully update user status",
            "data": updated_user,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_user: {str(e)}")
        return error_handler(e)

def get_all_users():
    try:
        users = user_model.get_all_users()
        if not users:
            return {"status": "success", "message": "No users found", "data": []}, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved users.",
            "data": users,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get user lists: {str(e)}")
        return error_handler(e)


def get_a_user(public_id):
    try:
        user = user_model.get_user_by_id(public_id)
        response_object = {
            "status": "success",
            "message": "Successfully get a user.",
            "data": user,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get user: {str(e)}")
        return error_handler(e)


def delete_user(public_id):
    try:
        user = user_model.delete_user(public_id)
        response_object = {
            "status": "success",
            "message": "Successfully delete user",
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_user: {str(e)}")
        return error_handler(e)

def user_auth(data):
    try:
        auth = user_model.user_auth(data)
        response_object = {
            "status": "success",
            "message": "Login Success",
<<<<<<< HEAD
<<<<<<< HEAD
            "token" : auth
=======
            "token" : auth,
            "data" : data
>>>>>>> 0969de1 (Add: User authentication)
=======
            "token" : auth
>>>>>>> d1abaf4 (Update: make endpoint update status require login)
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Login Error: {str(e)}")
        return error_handler(e)
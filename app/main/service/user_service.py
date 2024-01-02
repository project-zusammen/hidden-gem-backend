import logging as log
from app.main.model.user import User
from ..util.helper import error_handler

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


# def update_user(public_id, data):
#     try:
#         updated_user = user_model.update_user(public_id, data)
#         if not update_user:
#             response_object = {"status": "fail", "message": "User does not exist."}
#             return response_object, 409
#         else:
#             response_object = {
#                 "status": "success",
#                 "message": "Successfully update user",
#                 "data": updated_user,
#             }
#             return response_object, 201
#     except Exception as e:
#         log.error(f"Error in update_user: {str(e)}")
#         return {"status": "error", "message": "Internal Server Error"}, 500


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
        print(f"Error in get_all_users: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


# def get_a_user(public_id):
#     try:
#         user = user_model.get_user_by_id(public_id)
#         if not user:
#             response_object = {"status": "fail", "message": "user does not exist."}
#             return response_object, 409

#         response_object = {
#             "status": "success",
#             "message": "Successfully get a user.",
#             "data": user,
#         }
#         return response_object, 200
#     except Exception as e:
#         log.error(f"Error in get_a_user: {str(e)}")
#         return {"status": "error", "message": "Internal Server Error"}, 500


# def delete_user(public_id):
#     try:
#         user = user_model.delete_user(public_id)
#         if not user:
#             response_object = {"status": "fail", "message": "user does not exist."}
#             return response_object, 409
#         response_object = {
#             "status": "success",
#             "message": "Successfully deleted.",
#             "data": user,
#         }
#         return response_object, 201
#     except Exception as e:
#         log.error(f"Error in delete_user: {str(e)}")
#         return {"status": "error", "message": "Internal Server Error"}, 500

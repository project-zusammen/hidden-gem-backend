import logging as log
from app.main.model.bookmark import Bookmark
from app.main.util.helper import error_handler

bookmark_model = Bookmark()

def create_bookmark(data):
    try:
        bookmark = bookmark_model.create_bookmark(data)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": bookmark,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_bookmark: {str(e)}")
        return error_handler(e), 500


def get_bookmark_by_userid(user_id):
    try:
        bookmark = bookmark_model.get_bookmark_by_userid(user_id)
        response_object = {
            "status": "success",
            "message": "Successfully get a bookmarks.",
            "data": bookmark,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_a_bookmark: {str(e)}")
        return error_handler(e), 500

def delete_bookmark(public_id):
    try:
        bookmark = bookmark_model.delete_bookmark(public_id)
        if not bookmark:
            response_object = {"status": "fail", "message": "bookmark does not exist."}
            return response_object, 409
        response_object = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": bookmark,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_bookmark: {str(e)}")
        return error_handler(e), 500

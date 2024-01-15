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
        if len(bookmark) == 0:
            return {"status": "success", "message": "No bookmarks found", "data": []}, 200
        response_object = {
            "status": "success",
            "message": "Successfully get a bookmark.",
            "data": bookmark,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_a_bookmark: {str(e)}")
        return error_handler(e), 500

def delete_bookmark(public_id):
    try:
        _ = bookmark_model.delete_bookmark(public_id)
        response_object = {
            "status": "success",
            "message": "Successfully deleted."
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_bookmark: {str(e)}")
        return error_handler(e), 500

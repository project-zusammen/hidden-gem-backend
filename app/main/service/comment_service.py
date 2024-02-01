import logging as log
from app.main.model.comment import Comment

comment_model = Comment()


def get_all_comments():
    try:
        comments = comment_model.get_all_comments()
        if not comments:
            return {
                "status": "success",
                "message": "No comments found",
                "data": [],
            }, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved comments.",
            "data": comments,
        }
        return response_object, 200
    except Exception as e:
        print(f"Error in get_all_comments: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def get_a_comment(public_id):
    try:
        comment = comment_model.get_comment_by_id(public_id)
        if not comment:
            response_object = {"status": "fail", "message": "comment does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully get a comment.",
            "data": comment,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_a_comment: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def create_comment(data):
    try:
        comment = comment_model.create_comment(data)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": comment,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_comment: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def delete_comment(public_id):
    try:
        comment = comment_model.delete_comment(public_id)
        if not comment:
            response_object = {"status": "fail", "message": "comment does not exist."}
            return response_object, 409
        response_object = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": comment,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_comment: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_comment(public_id, data):
    try:
        updated_comment = comment_model.update_comment(public_id, data)
        if not update_comment:
            response_object = {"status": "fail", "message": "Comment does not exist."}
            return response_object, 409
        else:
            response_object = {
                "status": "success",
                "message": "Successfully updated.",
                "data": updated_comment,
            }
            return response_object, 201
    except Exception as e:
        log.error(f"Error in update_comment: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def upvote_comment(public_id, upvote=True):
    try:
        upvoted_comment = comment_model.upvote_comment(public_id, upvote)
        if not upvoted_comment:
            response_object = {"status": "fail", "message": "Comment does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully upvoted.",
            "data": upvoted_comment,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in upvote_comment: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_visibility(public_id, visible=True):
    try:
        updated_visibility = comment_model.update_visibility(public_id, visible)
        if not updated_visibility:
            response_object = {"status": "fail", "message": "Comment does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "data": updated_visibility,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_visibility: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500

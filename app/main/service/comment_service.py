import logging as log
from app.main.model.comment import Comment

comment_model = Comment()

def get_all_comments():
    try:
        comments = comment_model.get_all_comments()
        if not comments:
            return {"status": "success", "message": "No comments found", "data": []}, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved comments.",
            "data": comments,
        }
        return response_object, 200
    except Exception as e:
        print(f"Error in get_all_comments: {str(e)}")
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
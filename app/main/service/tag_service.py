import logging as log
from app.main.model.tag import Tag
from ..util.helper import error_handler

log.basicConfig(level=log.ERROR)

tag_model = Tag()


def create_tag(data):
    try:
        result = tag_model.create_tag(data)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": result,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_tag: {str(e)}")
        return error_handler(e)

def get_all_tags():
    try:
        result = tag_model.get_all_tags()
        response_object = {
            "status": "success",
            "message": "Successfully retrieved.",
            "data": result,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_all_tags: {str(e)}")
        return error_handler(e)
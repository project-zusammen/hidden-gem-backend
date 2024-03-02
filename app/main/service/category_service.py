import logging as log
from app.main.model.category import Category
from ..util.helper import error_handler

category_model = Category()


def create_category(category_name):
    try:
        category = category_model.create_category(category_name)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": category,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_category: {str(e)}")
        return error_handler(e)

def get_all_categories():
    try:
        categories = category_model.get_all_categories()
        if not categories:
            return {"status": "success", "message": "No categories found", "data": []}, 200
        
        response_object = {
            "status": "success",
            "message": "Successfully get.",
            "data": categories,
        }
        return response_object, 200
    except  Exception as e:
        log.error(f"Error in get_all_categories: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500
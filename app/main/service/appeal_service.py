import logging as log
from app.main.model.appeal import Appeal

appeal_model = Appeal()


def create_appeal(data):
    try:
        appeal = appeal_model.create_appeal(data)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": appeal,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_appeal: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500

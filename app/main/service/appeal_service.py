import logging as log
from app.main.model.appeal import Appeal

appeal_model = Appeal()


def get_all_appeals():
    try:
        appeals = appeal_model.get_all_appeals()
        if not appeals:
            return {
                "status": "success",
                "message": "No appeals found",
                "data": [],
            }, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved appeals.",
            "data": appeals,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_all_appeals: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def get_an_appeal(public_id, user_id, role):
    try:
        appeal = appeal_model.get_appeal_by_id(public_id, user_id, role)
        if not appeal:
            return {
                "status": "success",
                "message": "Appeal does not exist.",
            }, 200

        response_object = {
            "status": "success",
            "message": "Successfully get a appeal.",
            "data": appeal,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_an_appeal: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def create_appeal(data, user_id):
    try:
        data["user_id"] = user_id
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


def update_appeal(public_id, status):
    try:
        updated_appeal = appeal_model.update_appeal(public_id, status)
        if not updated_appeal:
            return {
                "status": "fail",
                "message": "Appeal does not exist.",
            }, 409
        response_object = {
            "status": "success",
            "message": "Successfully update appeal.",
            "data": updated_appeal,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_appeal: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500

import logging as log
from app.main.model.region import Region

region_model = Region()


def get_all_region():
    try:
        regions = region_model.get_all_regions()
        if not regions:
            return {"status": "success", "message": "No regions found"}, 409
        response_object = {
            "status": "success",
            "message": "Successfully retrieved users.",
            "data": regions,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get region lists: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def create_region(data):
    try:
        region = region_model.create_region(data)
        response_object = {
            "status": "success",
            "message": "Succesfully created.",
            "data": region,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_region: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_region(public_id, data):
    try:
        updated_region = region_model.update_region(public_id, data)
        if not updated_region:
            response_object = {"status": "fail", "message": "Region does not exist."}
            return response_object, 409
        else:
            response_object = {
                "status": "success",
                "message": "Succesfully created.",
                "data": updated_region,
            }
            return response_object, 201
    except Exception as e:
        log.error(f"Error in update_region: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def delete_region(public_id):
    try:
        region = region_model.get_region_by_id(public_id)
        if not region:
            response_object = {"status": "fail", "message": "Region does not exist."}
            return response_object, 409
        del_region = region_model.delete_region(public_id)
        response_object = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": del_region,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500

import logging as log
from app.main.model.report import Report

report_model = Report()


def create_report(data, user_id):
    try:
        data["user_id"] = user_id
        report = report_model.create_report(data)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": report,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_report: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def get_all_reports(page, count):
    try:
        reports = report_model.get_all_reports(page, count)
        if not reports:
            return {
                "status": "success",
                "message": "No reports found",
                "data": [],
            }, 200


        response_object = {
            "status": "success",
            "message": "Successfully retrieved reports.",
            "data": reports,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_all_reports: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500



def get_a_report(public_id, user_id, role):
    try:
        report = report_model.get_report_by_id(public_id, user_id, role)
        if not report:
            return {
                "status": "success",
                "message": "report does not exist.",
            }, 200

        response_object = {
            "status": "success",
            "message": "Successfully get a report.",
            "data": report,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_an_report: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_report(public_id, status):
    try:
        updated_report = report_model.update_report(public_id, status)
        if not updated_report:
            return {
                "status": "fail",
                "message": "Report does not exist.",
            }, 409
        response_object = {
            "status": "success",
            "message": "Successfully update report.",
            "data": updated_report,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_report: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500

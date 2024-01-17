import logging as log
from app.main.model.report import Report

report_model = Report()


def create_report(data):
    try:
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

from flask_restx import fields
from app.extensions import api

"""
DTO (Data Transfer Object) is a simple object which is used to pass data between software components.
"""


class ReviewDto:
    review = api.model(
        "review",
        {
            "title": fields.String(required=True, description="review title"),
            "content": fields.String(required=True, description="review content"),
            "location": fields.String(description="review location"),
            "category_id": fields.String(description="category Identifier"),
            "region_id": fields.String(description="region Identifier"),
        },
    )
    upvote = api.model(
        "upvote",
        {
            "upvote": fields.Boolean(description="upvote")
        }
    )
    visible = api.model(
        "visible",
        {
            "visible": fields.Boolean(description="visible")
        }
    )

class UserDto:
    user = api.model(
        "user",
        {
            "username": fields.String(required=True, description="username"),
            "email": fields.String(required=True, description="user email"),
            "password": fields.String(required=True, description="user password")
        },
    )
    status = api.model(
        "status",
        {
            "banned": fields.Boolean(required=True, description="user status that want to be updated")
        }
    )

class ReportDto:
    report = api.model(
        "report",
        {
            "type": fields.String(required=True, description="report type"),
            "item_id": fields.String(required=True, description="report item_id"),
            "reason": fields.String(required=True, description="report reason"),
        },
    )
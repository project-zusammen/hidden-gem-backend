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
    upvote = api.model("upvote", {"upvote": fields.Boolean(description="upvote")})

    visible = api.model("visible", {"visible": fields.Boolean(description="visible")})


class UserDto:
    user = api.model(
        "user",
        {
            "username": fields.String(required=True, description="username"),
            "email": fields.String(required=True, description="user email"),
            "password": fields.String(required=True, description="user password"),
        },
    )
    login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email for login"),
            "password": fields.String(
                required=True, description="user password for login"
            ),
        },
    )
    status = api.model(
        "status",
        {
            "banned": fields.Boolean(
                required=True, description="user status that want to be updated"
            )
        },
    )


class CommentDto:
    comment = api.model(
        "comment",
        {
            "content": fields.String(required=True, description="comment content"),
            "review_id": fields.String(required=True, description="review Identifier"),
        },
    )
    upvote = api.model("upvote", {"upvote": fields.Boolean(description="upvote")})
    visible = api.model("visible", {"visible": fields.Boolean(description="visible")})


class RegionDto:
    region = api.model(
        "region",
        {"city": fields.String(required=True, description="city name for region")},
    )


class AppealDto:
    appeal = api.model(
        "appeal",
        {
            "appeal": fields.String(required=True, description="reason for appeal"),
            "report_id": fields.String(required=True, description="report Identifier"),
        },
    )
    status = api.model("status", {"status": fields.Boolean(description="status")})

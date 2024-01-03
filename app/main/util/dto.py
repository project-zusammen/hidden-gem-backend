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

class UserDto:
    user = api.model(
        "user",
        {
            "username": fields.String(required=True, description="username"),
            "email": fields.String(required=True, description="user email"),
            "password": fields.String(required=True, description="user password")
        },
    )
    login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email for login"),
            "password": fields.String(required=True, description="user password for login")
        },
    )
    status = api.model(
        "status",
        {
            "banned": fields.Boolean(required=True, description="username"),
        }
    )


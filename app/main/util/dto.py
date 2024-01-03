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
<<<<<<< HEAD

class LoginDto:
    login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email for login"),
            "password": fields.String(required=True, description="user password for login")
        },
    )
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 92aca57 (Add: User authentication endpoint dto)
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
            "banned": fields.Boolean(required=True, description="user status that want to be updated"),
        }
<<<<<<< HEAD
    )
=======
    )
=======

<<<<<<< HEAD
>>>>>>> 31c359a (Add: User authentication endpoint)
=======
=======
=======
>>>>>>> c5a2fa1 (Add: User authentication endpoint dto)
    status = api.model(
        "status",
        {
            "banned": fields.Boolean(required=True, description="username"),
        }
    )
<<<<<<< HEAD
>>>>>>> 2145c43 (Update: modifying update status endpoint to receive status input)
>>>>>>> e1472c5 (Update: modifying update status endpoint to receive status input)
=======

>>>>>>> c5a2fa1 (Add: User authentication endpoint dto)
>>>>>>> 92aca57 (Add: User authentication endpoint dto)

from datetime import datetime, timedelta
import time
import email_validator
from werkzeug.security import generate_password_hash
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

secretKey = os.getenv("SECRET_KEY")



def convert_to_local_time(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


def hash_password(password):
    return generate_password_hash(password)


def is_valid_email(email):
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False


def error_handler(error):
    message = ""
    error_message = str(error)
    if "The email is invalid" in error_message:
        message = f"Registration failed : {error_message}"

    elif "This email has already registered" in error_message:
        message = f"Register user failed : Your email is already registered"

    elif "Duplicate entry" in error_message:
        message = f"Insert data failed : Data already exist, cannot duplicate data"

    elif "not found" in error_message:
        message = f"Error retrieve data : {error_message}"

    elif "Incorrect password" in error_message:
        message = f"Login Failed : {error_message}"

    elif "Access denied" in error_message:
        message = f"Access denied: You are not authorized for this operation"

    else:
        message = "Internal Server Error"

    return {"status": "error", "message": message}, 500

def create_token(user):
    token = jwt.encode(
        {
            "id": user["id"],
            "public_id": user["public_id"],
            "email": user["email"],
            "role": user["role"],
            "username": user["username"],
            "status": user["status"],
            "exp": datetime.utcnow() + timedelta(days=1),
        },
        secretKey,
    )
    return token

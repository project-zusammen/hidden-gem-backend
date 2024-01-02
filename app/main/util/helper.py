from datetime import datetime
import time
import email_validator
from werkzeug.security import generate_password_hash, check_password_hash

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

    elif "Duplicate entry" in error_message:
        message = f"Insert data failed : Data already exist, cannot duplicate data"
    
    else: 
        message = "Internal Server Error"

    return {
        "status": "error", 
        "message": message
    }, 500

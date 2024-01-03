import jwt
import os
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps
<<<<<<< HEAD
=======
from app.main.model.user import User
>>>>>>> 0969de1 (Add: User authentication)

from app.main.model.user import User

load_dotenv()

secretKey = os.getenv("SECRET_KEY")

# decorator for verifying the JWT
def token_required(f):
<<<<<<< HEAD
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers.get('X-API-KEY')
        if not token:
            return {'message': 'Access Denied: Unauthorized operation. Please log in to proceed.'}, 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secretKey, algorithms=["HS256"])
            
            return f(decoded_token=data,*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return {'message': 'Your current session has expired. Please log in again to continue.'}, 401
        except Exception as e:
            print(f"Error: {str(e)}")
            return {'message': 'Access Denied: Token is invalid'}, 401

    return decorated

=======

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secretKey)
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated
>>>>>>> 0969de1 (Add: User authentication)

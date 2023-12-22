from app.main.model.user import Users
from app.main.view import response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from app import db
import uuid

def getUsers():
    try:
        users = Users.query.all()
        data = collectUserData(users)
        return response.ok(data, "Success Get User lists")
    except Exception as e:
        print(f"Error: {e}") 
        return response.badRequest([], f'Error : {e}')


def collectUserData(users):
    array = []
    for user in users:
        array.append(formatUserData(user))
    return array

def formatUserData(user):
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.value
    }
    return data

def getUserById(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest([], 'User Not Found')

        data = formatUserData(users)
        return response.ok(data, "Success get user by id")
    except Exception as e:
        print(f"Error: {e}")  
        return response.badRequest([], f'Error : {e}')

def createUser():
    try:
        random_uuid = str(uuid.uuid4())
        
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if not username or not email or not password:
            return response.badRequest([], 'Error : The input is incomplete. Please make sure to fill the username, email and password')

        hashed_password = generate_password_hash(password)

        new_user = Users(uuid=random_uuid, username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Successfully create user!'}), 200

    except Exception as e:
        print(e)
        return response.badRequest([], f'Error : {e}')


def updateUser(id):
    try:
        print("test")
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        hashed_password = generate_password_hash(password)

        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'User Not Found')

        user.email = email
        user.username = username
        user.password = hashed_password

        db.session.commit()
        return response.ok('', 'Successfully update data!')

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return response.badRequest([], f'Error : {e}')


def deleteUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'User Not Found')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        return response.badRequest([], f'Error : {e}')


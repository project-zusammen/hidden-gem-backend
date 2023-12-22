from app import app
from app.main.controller import UserController
from flask import request

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return UserController.getUsers()
    else:
        return UserController.createUser()

@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.getUserById(id)
    elif request.method == 'PUT':
        return UserController.updateUser(id)
    elif request.method == 'DELETE':
        return UserController.deleteUser(id)
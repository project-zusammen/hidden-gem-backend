from app import app
from app.main.controller import userController
from flask import request

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return userController.getUsers()
    else:
        return userController.createUser()

@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return userController.getUserById(id)
    elif request.method == 'PUT':
        return userController.updateUser(id)
    elif request.method == 'DELETE':
        return userController.deleteUser(id)
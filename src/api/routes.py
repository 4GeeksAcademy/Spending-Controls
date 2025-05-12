"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Employee, Bill, Department, Budget
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login_user():
    body = request.get_json()

    if body['email'].strip() == "" or body["password"].strip() == "":
        return jsonify({"msg": "fields cannot be empty"}), 400

    email = body['email']
    user = Employee.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    password = body["password"]

    # password_hashed = bcrypt.check_password_hash(user.password,password)
    # if not password_hashed:
    #     return jsonify({"msg":"Incorrect data"}),404

    if user.password != password:
        return jsonify({"msg": "Incorrect data"}), 404

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 201

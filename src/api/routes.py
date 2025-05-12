"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Employee, Bill, Department, Budget
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
import re

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

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if re.match(pattern, email) is None:
        return jsonify({"msg": "The email format is not valid"}), 400

    password = body["password"]

    if len(password) < 8:
        return jsonify({"msg": "Invalid credentials"}), 401

    user = Employee.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Invalid credentials"}), 401

    # password_hashed = bcrypt.check_password_hash(user.password,password)
    # if not password_hashed:
    #     return jsonify({"msg":"Incorrect data"}),404

    if user.password != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 201

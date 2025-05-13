"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Employee, Bill, Department, Budget
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)
# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if data is None:
         return jsonify({"Error": "Data Not Provided"}), 400
    
    name = data.get("name", None)
    last_name = data.get("last_name", None)
    email = data.get("email", None)
    password = data.get("password", None)
    is_supervisor = data.get("is_supervisor", False)
   
    
    if not email or not password:
        return jsonify({"Error": "Email and Password are required"}), 400
    
    #check if an employee already exist 
    existing_employee = Employee.query.filter_by(email = email).first()
    if existing_employee:
        return jsonify({"Msg": "Employee already exists. Please go to login."}), 409
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #Create new user with the data obtained
    new_employee = Employee(
        name = name, 
        last_name = last_name, 
        email = email, 
        password = hashed_password,
        is_supervisor = is_supervisor,
        is_active = True)

    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"msg": "New employee created",
                    "employee": new_employee.serialize()
                    }), 201




@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

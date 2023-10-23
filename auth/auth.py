from . import auth_obj
from model.database import *
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt

from control.auth_check import *

@auth_obj.route('/api/user', methods=['POST'])
def signup():
    data_json = request.get_json()
    name = data_json['name']
    email = data_json['email']
    password = data_json['password']
       
    query = "SELECT * FROM member WHERE email = (%s)"
    data = (email,)
    results = execute_query_read(query, data)

    if len(results) == 1: # ok so how to set up that data is None? 
        response = {
            "error": True,
            "message": "This email was registered before."
        }
        return jsonify(response), 400
    else:
        query = "INSERT INTO member(name, email, password) VALUES(%s, %s, %s);"
        data = (name, email, password)
        if execute_query_create(query, data):
            response = {
                "ok": True
            }
            return jsonify(response), 200
        else:
            response = {
                "error": True,
                "message": "SQL database internal issue"
            }
            return jsonify(response), 500
        


@auth_obj.route('/api/user/auth', methods=['PUT'])
def signin():
    data_json = request.get_json()
    email = data_json['email']
    password = data_json['password']
    
    query = "SELECT * FROM member WHERE email = (%s)"
    data = (email,)
    
    results = execute_query_read(query, data)
    
    # print("check point 1")
    # print(results)
    
    if results == "error":
        response = {
            "error": True,
            "message": "Database has an internal issue."
        }
        return jsonify(response), 500
    else:
        password_from_sql = results[0]["password"]
        results = results[0]
    
    if password == password_from_sql:
        payload_data = {
            "id": results['id'],
            "name": results['name'],
            "email": results['email'],
            "password": results['password'],
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        
        expiration_time = timedelta(days=7)
        
        token = jwt.encode(
            payload = payload_data,
            key = os.getenv('jwt_key'),
            algorithm = os.getenv('jwt_algorithm'),
        )
        
        return jsonify({"token": token}), 200
    else:
        response = {
            "error": True,
            "message": "Wrong password!"
        }
        return jsonify(response), 400
    

@auth_obj.route('/api/user/auth', methods=['GET'])
def signin_get():
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401  # Unauthorized

    token_type, token = auth_header.split()
    if token_type != os.getenv('token_type'):
        return jsonify({"error": "Invalid token type"}), 401  # Unauthorized
    try:
        # Verify and decode the token
        payload = jwt.decode(token, os.getenv('jwt_key'), algorithms=[os.getenv('jwt_algorithm')])
        # print(payload)
        # Token is valid, user is logged in
        return jsonify({"data": payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401  # Unauthorized
    except jwt.DecodeError:
        return jsonify({"error": "Invalid token"}), 401  # Unauthorized
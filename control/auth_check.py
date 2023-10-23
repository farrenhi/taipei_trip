from model.database import *
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
import requests

def auth_check(item):
    if not item:
        return False
    
    token_type, token = item.split()
    if token_type != os.getenv('token_type'):
        return False
    try:
        payload = jwt.decode(token, os.getenv('jwt_key'), algorithms=[os.getenv('jwt_algorithm')])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False

def return_login_failure(item):
    response ={
        "error": True,
        "message": "to be continued"
    }
    
    if not auth_check(item):
        response["message"] = "Login Status Check Failure"
        return jsonify(response), 403
    
    
def connect_tappay(prime, cardholder):
    # Define the URL
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

    # Define the request payload
    payload = {
        "prime": prime,
        "partner_key": os.getenv('partner_key'),
        "merchant_id": "testandtest_TAISHIN",
        "details": "TapPay Test",
        "amount": 1,
        "cardholder": cardholder,
        "remember": False
    }

    # Define headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv('x-api-key'),
    }

    # Make the request
    response = requests.post(url, json=payload, headers=headers)

    # Print the response
    response_json = response.json()
    return response_json
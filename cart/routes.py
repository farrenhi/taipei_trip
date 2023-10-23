# # Define routes and views for this blueprint
from flask import *
from model.database import *
from control.auth_check import *
from . import booking

@booking.route('/api/booking', methods=['POST'])
def booking_post():
    auth_header = request.headers.get('Authorization')
    
    response ={
        "error": True,
        "message": "to be continued"
    }
    
    if not auth_check(auth_header):
        response["message"] = "Login Status Check Failure"
        return jsonify(response), 403

    try:
        data_json = request.get_json()
        session.setdefault('cart', {})
        
        cart = session['cart']
        cart['attractionId'] = data_json['attractionId']
        cart['date'] = data_json['date']
        cart['time'] = data_json['time']
        cart['price'] = data_json['price']
        session['cart'] = cart
        print("session['cart']: ", session['cart'])
        response = {"ok": True}
        return jsonify(response), 200
    except KeyError as e:
        error_message = f'Missing key in request data: {e}'
        response["message"] = error_message
        return jsonify(response), 400
    except Exception as e:
        error_message = f'An error occurred: {e}'
        response["message"] = error_message
        return jsonify(response), 500


@booking.route('/api/booking', methods=['GET'])
def booking_get():
    auth_header = request.headers.get('Authorization')
    
    if not auth_check(auth_header):
        response = {
            "error": True,
            "message": "to be continued"
        }
        response["message"] = "Login Status Check Failure"
        return jsonify(response), 403
    
    # print(session)
    # sight_id = session['cart']['attractionId']
    # if session['cart']['attractionId']:
    if 'cart' in session and 'attractionId' in session['cart'] and session['cart']['attractionId']:
        sight_id = session['cart']['attractionId']
        data_backend = get_attraction_lookup(sight_id)
        response = {
        "attraction": data_backend[0],
        "date": session['cart'].get("date"),
        "time": session['cart'].get("time"),
        "price": session['cart'].get("price"),   
        }
    else:
        response = None

    # print(response)
    return jsonify({"data": response}), 200




@booking.route('/api/booking', methods=['DELETE'])
def booking_delete():
    auth_header = request.headers.get('Authorization')
    
    if not auth_check(auth_header):
        response = {
            "error": True,
            "message": "to be continued"
        }
        response["message"] = "Login Status Check Failure"
        return jsonify(response), 403
    session.clear()
    print(session)
    
    # sight_id = session['cart']['attractionId']

    # if sight_id:
    #     data_backend = get_attraction_lookup(sight_id)
    # else:
    #     data_backend["data"] = None
    
    # response = {
    #     "attraction": data_backend[0],
    #     "date": session['cart'].get("date"),
    #     "time": session['cart'].get("time"),
    #     "price": session['cart'].get("price"),   
    # }

    return jsonify({"ok": True}), 200



@booking.route('/api/orders', methods=['POST'])
def orders_post():
    auth_header = request.headers.get('Authorization')
    return_login_failure(auth_header)
    # if not auth_check(auth_header):
    #     response = {
    #         "error": True,
    #         "message": "to be continued"
    #     }
    #     response["message"] = "Login Status Check Failure"
    #     return jsonify(response), 403
           
    data_json = request.get_json()
    prime = data_json['prime']

    current_datetime = datetime.now()
    order_number = current_datetime.strftime("%Y%m%d%H%M%S%f") + str(data_json['member_login_id'])
    
    query = "INSERT INTO orders(order_number, contact_name, contact_email, contact_phone, \
             payment_status, price, sight_id, member_id, trip_date, trip_time) \
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (order_number, 
            data_json['contact']['name'], 
            data_json['contact']['email'],
            data_json['contact']['phone'],
            0,
            data_json['order']['price'],
            data_json['order']['trip']['attraction']['id'], 
            data_json['member_login_id'],
            data_json['order']['date'],
            data_json['order']['time'],
            )
    
    if execute_query_create(query, data):
        # print("new order created in SQL database")
        pass
    else:
        response = {
            "error": True,
            "message": "SQL database issue: booking order is not created."
        }
        return jsonify(response), 500
        
    # call TapPay API for payment process
    cardholder = {
        "phone_number": data_json['contact']['phone'],
        "name": data_json['contact']['name'],
        "email": data_json['contact']['email'],
    }
    
    
    response_tappay = connect_tappay(prime, cardholder)
    json_response = json.dumps(response_tappay)
    # print(response_tappay)
    # print(type(response_tappay))
    
    query = "UPDATE orders SET payment_memo = %s WHERE order_number = %s"
    data = (json_response, order_number)
    if execute_query_update(query, data):
        # print("payment info recorded")
        pass
    else:
        response = {
            "error": True,
            "message": "SQL database is not updated with payment process info"
        }
        return  jsonify(response), 500
    
    if response_tappay['status'] == 0:
        query = "UPDATE orders SET payment_status = %s WHERE order_number = %s"
        data = (1, order_number)
        execute_query_update(query, data)
        session.clear()
        # print("payment status is set to 1. Paid!")
        
    response_frontend = {"data": {
        "number": order_number,
        "payment": {
            "status": response_tappay['status'],
            "message": "payment processed"
        }
    }}
    return jsonify(response_frontend), 200



    
@booking.route('/api/order/<int:order_number>', methods=['GET'])
def orders_get(order_number):
    auth_header = request.headers.get('Authorization')
    return_login_failure(auth_header)
    
    query = "SELECT * FROM orders WHERE order_number = (%s)"
    data = (order_number,)
    result = execute_query_read(query, data)
    if result:
        order_data = result[0]  # Assuming there's only one result
        sight_info = get_attraction_lookup(order_data["sight_id"])[0]
        
        formatted_data = {
            "data": {
                "number": order_data["order_number"],
                "price": order_data["price"],
                "trip": {
                    "attraction": {
                        "id": order_data["sight_id"],
                        "name": sight_info["name"],
                        "address": sight_info["address"],
                        "image": sight_info["image"]
                    },
                    "date": order_data["trip_date"].strftime("%Y-%m-%d"),
                    "time": order_data["trip_time"].lower()
                },
                "contact": {
                    "name": order_data["contact_name"],
                    "email": order_data["contact_email"],
                    "phone": order_data["contact_phone"]
                },
                "status": int(order_data["payment_status"])  # Convert to integer
            }
        }
        return jsonify(formatted_data), 200
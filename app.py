from flask import *
import jwt
from datetime import datetime, timedelta
app=Flask(__name__)



app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/static",
)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = 'your_secret_key'



# Connection Pool
import mysql.connector.pooling

# Configuration for the database connection pool
# db_config_haha = {
#     "host": "localhost",
#     "user": "root",
#     "password": "MyNewPass5!",
#     "database": "mydb",
#     "port": 3306,
# }

# local parameters
db_config_haha = {
    "host": "localhost",
    "user": "root",
    "password": "MyNewPass5!",
    "database": "mydb",
}


# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config_haha)

# Functions to execute a query using a connection from the pool
def execute_query_create(query, data=None):
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, data)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Error:", e)
        return False
    finally:
        cursor.close()
        connection.close()

def execute_query_read(query, data=None):
    # To request a connection from the pool, use its get_connection() method: 
    connection = connection_pool.get_connection() 
    cursor = connection.cursor(dictionary=True)
    
    mycursor = connection.cursor(dictionary=True)
    set_session_query = "SET SESSION group_concat_max_len = 1000000;"
    mycursor.execute(set_session_query)
    
    myresult = None
    try:
        cursor.execute(query, data)
        myresult = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        myresult = "error"
    finally:
        cursor.close()
        mycursor.close()
        connection.close()
        return myresult

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route('/api/mrts', methods=["GET"])
def mrts():
    # Insert category if not already present
    query_40sights = """
    SELECT m.name as mrt_name, COUNT(*) as num_sights
    FROM sight s
    JOIN mrt m ON s.mrt_id = m.id
    GROUP BY mrt_name
    ORDER BY num_sights DESC;
    """
    myresult = execute_query_read(query_40sights)
    
    if myresult is None:
        response = {
            "error": True,
            "message": "MRT names data is not properly read from SQL database."
        }
        return jsonify(response), 500
    else:    
        response = {"data": [result['mrt_name'] for result in myresult]} # mrt_names
        return jsonify(response)

# Version 12: put all url links into one key-value pair
def format_attraction_data(results):
    formatted_results = []
    current_sight = None

    for row in results:
        if current_sight is None or current_sight['id'] != row['id']:
            if current_sight is not None:
                formatted_results.append(current_sight)
            current_sight = {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "description": row["description"],
                "address": row["address"],
                "transport": row["transport"],
                "mrt": row["mrt"],
                "lat": row["lat"],
                "lng": row["lng"],
                "images": [] if row["images"] is None else row["images"].split(',')
            }
        else:
            if row["images"]:
                current_sight["images"].extend(row["images"].split(','))

    if current_sight is not None:
        formatted_results.append(current_sight)

    return formatted_results

# get all sights data in 12 data entry
@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    page = int(request.args.get('page', 0))  # Get the requested page number
    keyword = request.args.get('keyword', '')

    per_page = 12  # Number of items per page
    offset = page * per_page

    # Prepare the SQL query
    query = """
        SELECT
            s.id,
            s.name,
            c.name AS category,
            s.description,
            s.address,
            s.transport,
            m.name AS mrt,
            s.lat,
            s.lng,
            GROUP_CONCAT(f.url) AS images
        FROM
            sight s
        JOIN
            category c ON s.category_id = c.id
        JOIN
            mrt m ON s.mrt_id = m.id
        LEFT JOIN
            file f ON s.id = f.sight_id
    """

    if keyword:
        query += " WHERE m.name = %s OR s.name LIKE %s"
        keyword_param = f"%{keyword}%"
        data = (keyword, keyword_param, per_page + 1, offset)
    else:
        data = (per_page + 1, offset)

    query += """
        GROUP BY s.id
        LIMIT %s OFFSET %s
    """

    # Fetch data from the database
    results = execute_query_read(query, data)

    # Prepare the response data
    if results is None or results == "error":
        response = {
            "error": True,
            "message": "Sight data is not properly read from SQL database."
        }
        return jsonify(response), 500
    else:
        formatted_results = format_attraction_data(results)  # Use the function
        # print(formatted_results)
        if len(formatted_results) == 13:
            
            # data back from sql is array. so the last element in array is max id.
            # arr.pop
            max_id_entry = max(formatted_results, key=lambda x: x["id"])
            formatted_results.remove(max_id_entry)  # use pop do not use remove.
            
            response = {
                "nextPage": page + 1,
                "data": formatted_results
            }

        else:
            response = {
            "nextPage": None,
            "data": formatted_results
            }
    
        return jsonify(response)

# single sight version 1:
@app.route('/api/attraction/<int:attractionId>', methods=['GET'])
def get_attraction(attractionId):
    # Prepare the SQL query to fetch attraction data by ID
    query = """
        SELECT
            s.id,
            s.name,
            c.name AS category,
            s.description,
            s.address,
            s.transport,
            m.name AS mrt,
            s.lat,
            s.lng,
            GROUP_CONCAT(f.url) AS images
        FROM
            sight s
        JOIN
            category c ON s.category_id = c.id
        JOIN
            mrt m ON s.mrt_id = m.id
        LEFT JOIN
            file f ON s.id = f.sight_id
        WHERE
            s.id = %s
        GROUP BY
            s.id
    """

    data = (attractionId,)

    # Fetch attraction data from the database
    results = execute_query_read(query, data)

    # Prepare the response data
    if results is None or len(results) == 0:
        response = {
            "error": True,
            "message": f"Attraction with ID {attractionId} not found."
        }
        return jsonify(response), 400
    
    elif results == "error":
        response = {
            "error": True,
            "message": "Database is not working properly."
        }
        return jsonify(response), 500
    
    else:
        formatted_attraction = format_attraction_data(results)
        response = {
            "data": formatted_attraction[0]
        }
        return jsonify(response)


@app.route('/api/user', methods=['POST'])
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

@app.route('/api/user/auth', methods=['PUT'])
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
            key = 'secret',
            algorithm="HS256",
        )
        
        return jsonify({"token": token}), 200
    else:
        response = {
            "error": True,
            "message": "Wrong password!"
        }
        return jsonify(response), 400
        
        

@app.route('/api/user/auth', methods=['GET'])
def signin_get():
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401  # Unauthorized
    # Check if the header starts with 'Bearer'
    token_type, token = auth_header.split()
    if token_type != 'Bearer':
        return jsonify({"error": "Invalid token type"}), 401  # Unauthorized
    try:
        # Verify and decode the token
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        # print(payload)
        # Token is valid, user is logged in
        return jsonify({"data": payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401  # Unauthorized
    except jwt.DecodeError:
        return jsonify({"error": "Invalid token"}), 401  # Unauthorized

def auth_check(item):
    if not item:
        return False
    
    token_type, token = item.split()
    if token_type != 'Bearer':
        return False
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False
    
@app.route('/api/booking', methods=['POST'])
def booking_post():
    auth_header = request.headers.get('Authorization')
    
    response ={
        "error": True,
        "message": "to be continued"
    }
    
    if not auth_check(auth_header):
        response["message"] = "Login Status Check Failure"
        return jsonify(response), 403
    else:
        print("good token! API checked the token again")
        
        
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


@app.route('/api/booking', methods=['GET'])
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
    
def get_attraction_lookup(attractionId):
    # Prepare the SQL query to fetch attraction data by ID
    query = """
        SELECT
            s.id,
            s.name,
            s.address,
            SUBSTRING_INDEX(GROUP_CONCAT(f.url), ',', 1) AS image
        FROM
            sight s
        JOIN
            category c ON s.category_id = c.id
        JOIN
            mrt m ON s.mrt_id = m.id
        LEFT JOIN
            file f ON s.id = f.sight_id
        WHERE
            s.id = %s
        GROUP BY
            s.id
    """
    data = (attractionId,)
    # Fetch attraction data from the database
    results = execute_query_read(query, data)
    return results
    # s.lat,
    # s.lng,
                # s.transport,
            # m.name AS mrt,
                        # s.description,
                                    # c.name AS category,
                                    # GROUP_CONCAT(f.url) AS images

@app.route('/api/booking', methods=['DELETE'])
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

app.run(host="0.0.0.0", port=3000, debug=True)
from flask import *
app=Flask(__name__)


app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/static",
)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True




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
    "database": "mydb2",
}


# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config_haha)

# Function to execute a query using a connection from the pool
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
    
app.run(host="0.0.0.0", port=3000, debug=True)
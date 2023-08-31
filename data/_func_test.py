# Connection Pool
import mysql.connector.pooling

# Configuration for the database connection pool
db_config_haha = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "mydb",
}

# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config_haha)

# Function to execute a query using a connection from the pool
def execute_query_read(query, data=None):
    
    # To request a connection from the pool, use its get_connection() method: 
    connection = connection_pool.get_connection() 
    cursor = connection.cursor(dictionary=True)
    myresult = None
    
    try:
        cursor.execute(query, data)
        myresult = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()
        return myresult


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
    # print(myresult[0]['mrt_name'])
    mrt_names = [result['mrt_name'] for result in myresult]
    # print(mrt_names)
    return mrt_names

print(mrts())



@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    page = int(request.args.get('page', 0))  # Get the requested page number
    keyword = request.args.get('keyword', '')

    per_page = 12  # Number of items per page
    offset = page * per_page

    # Prepare the base SQL query
    query = "SELECT * FROM your_table"

    if keyword:
        # If keyword is provided, add a WHERE clause for filtering
        query += " WHERE station_name = %s OR spot_name LIKE %s"
        keyword_param = f"%{keyword}%"

        data = (keyword, keyword_param, per_page, offset)
    else:
        data = (per_page, offset)

    query += " LIMIT %s OFFSET %s"

    # Fetch data from the database
    results = execute_query_read(query, data)

    # Prepare the response data
    response = {
        "nextPage": page + 1,
        "data": results
    }

    return jsonify(response)



# # version 11: normal one, but only 1 image url
# @app.route('/api/attractions', methods=['GET'])
# def get_attractions():
#     page = int(request.args.get('page', 0))  # Get the requested page number
#     keyword = request.args.get('keyword', '')

#     per_page = 12  # Number of items per page
#     offset = page * per_page

#     # Prepare the base SQL query
#     query = """
#         SELECT
#             s.id,
#             s.name,
#             c.name AS category,
#             s.description,
#             s.address,
#             s.transport,
#             m.name AS mrt,
#             s.lat,
#             s.lng,
#             f.url AS image
#         FROM
#             sight s
#         JOIN
#             category c ON s.category_id = c.id
#         JOIN
#             mrt m ON s.mrt_id = m.id
#         LEFT JOIN
#             file f ON s.id = f.sight_id
#     """

#     if keyword:
#         query += " WHERE s.name = %s OR s.name LIKE %s"
#         keyword_param = f"%{keyword}%"
#         data = (keyword, keyword_param, per_page, offset)
#     else:
#         data = (per_page, offset)

#     query += """
#         LIMIT %s OFFSET %s
#     """

#     # Fetch data from the database
#     results = execute_query_read(query, data)

#     # Prepare the response data
#     if results is None:
#         response = {
#             "error": True,
#             "message": "Sight data is not properly read from SQL database."
#         }
#     else:
#         response = {
#             "nextPage": page + 1,
#             "data": results
#         }
#     return jsonify(response)



def format_attraction_data(results):
    formatted_results = []
    current_attraction = None

    for row in results:
        if current_attraction is None or current_attraction['id'] != row['id']:
            if current_attraction is not None:
                formatted_results.append(current_attraction)
            current_attraction = {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "description": row["description"],
                "address": row["address"],
                "transport": row["transport"],
                "mrt": row["mrt"],
                "lat": row["lat"],
                "lng": row["lng"],
                "images": [row["image"]] if row["image"] else []
            }
        else:
            if row["image"]:
                current_attraction["images"].append(row["image"])

    if current_attraction is not None:
        formatted_results.append(current_attraction)

    return formatted_results[0] if formatted_results else None



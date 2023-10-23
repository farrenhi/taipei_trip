# # Define routes and views for this blueprint
from flask import *
from model.database import *
from . import sights

@sights.route('/api/mrts', methods=["GET"])
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


# get all sights data in 12 data entry
@sights.route('/api/attractions', methods=['GET'])
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
@sights.route('/api/attraction/<int:attractionId>', methods=['GET'])
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
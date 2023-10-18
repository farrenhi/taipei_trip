from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

# Connection Pool
import mysql.connector.pooling

# local parameters
db_config_haha = os.getenv('db_config_haha')
db_config_haha = eval(db_config_haha)


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

def execute_query_update(query, data=None):
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

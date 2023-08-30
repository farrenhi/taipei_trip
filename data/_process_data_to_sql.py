import json, sys, re
# Connection Pool
import mysql.connector.pooling

# Assuming you have a JSON file named "taipei-attractions.json"
with open('taipei-attractions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Set standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Now you can print the data containing Unicode characters




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


# Insert category if not already present
query_40sights = """
SELECT m.name as mrt_name, COUNT(*) as num_sights
FROM sight s
JOIN mrt m ON s.mrt_id = m.id
GROUP BY mrt_name
ORDER BY num_sights DESC;
"""
execute_query_read(query_40sights, (,))



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


# print(data['result']['results'][0]['direction'])
# print(data['result']['results'][0])
# mrt_name = "新北投"
# mrt_id_query = "SELECT id FROM mrt WHERE name = %s"
# mrt_id = execute_query_read(mrt_id_query, (mrt_name,))[0]['id']
# print(execute_query_read(mrt_id_query, (mrt_name,))[0]['id'])

# Loop through the JSON data

# Function to extract JPG URLs from a string
def extract_jpg_urls(string):
    pattern = r"https?://[^\s]+?\.[jJ][pP][eE]?[gG]"
    matches = re.findall(pattern, string)
    return matches

# for entry in data['result']['results']:
#     # Extract relevant data from the entry
    
#     id = entry['_id']
#     name = entry['name']
#     description = entry['description']
#     address = entry['address']
#     transport = entry['direction']  # Assuming 'direction' corresponds to 'transport' in the database
#     lat = float(entry['latitude'])
#     lng = float(entry['longitude'])
#     if entry['MRT'] is None:
#         mrt_name = 'No MRT station'
#     else:
#         mrt_name = entry['MRT']
#     category_name = entry['CAT']
#     file_urls = entry['file'].split(' ')  # Assuming file URLs are space-separated



#     # Insert MRT station if not already present
#     mrt_query = "INSERT IGNORE INTO mrt (name) VALUES (%s)"
#     execute_query_update(mrt_query, (mrt_name,))

#     # Insert category if not already present
#     category_query = "INSERT IGNORE INTO category (name) VALUES (%s)"
#     execute_query_update(category_query, (category_name,))

#     # Get MRT and category IDs
#     mrt_id_query = "SELECT id FROM mrt WHERE name = %s"
#     category_id_query = "SELECT id FROM category WHERE name = %s"
    
#     mrt_id = execute_query_read(mrt_id_query, (mrt_name,))[0]['id']
#     category_id = execute_query_read(category_id_query, (category_name,))[0]['id']
#     # print(id, name, mrt_id, mrt_name, category_id, category_name)
#     # print(name, description, address, transport, lat, lng, mrt_id, category_id)

#     # Insert sight
#     sight_query = "INSERT INTO sight (id, name, description, address, transport, lat, lng, mrt_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     execute_query_update(sight_query, (id, name, description, address, transport, lat, lng, mrt_id, category_id))

#     # Get sight ID
#     sight_id_query = "SELECT id FROM sight WHERE name = %s"
#     # sight_id = execute_query_read(sight_id_query, (name,))[0]['id']

#     # Insert file URLs
#     for url in file_urls:
#         file_query = "INSERT INTO file (sight_id, url) VALUES (%s, %s)"
#         execute_query_update(file_query, (sight_id, url))

# Iterate through JSON entries
for entry in data['result']['results']:
    id = entry['_id']
    name = entry['name']
    description = entry['description']
    address = entry['address']
    transport = entry['direction']  # Assuming 'direction' corresponds to 'transport' in the database
    lat = float(entry['latitude'])
    lng = float(entry['longitude'])
    if entry['MRT'] is None:
        mrt_name = 'No MRT station'
    else:
        mrt_name = entry['MRT']
    category_name = entry['CAT']
    file_urls = entry['file'].split(' ')  # Assuming file URLs are space-separated
    
    # Insert MRT station if not already present
    mrt_query = "INSERT IGNORE INTO mrt (name) VALUES (%s)"
    execute_query_update(mrt_query, (mrt_name,))
    
    # Insert category if not already present
    category_query = "INSERT IGNORE INTO category (name) VALUES (%s)"
    execute_query_update(category_query, (category_name,))
    
    # Get MRT and category IDs
    mrt_id_query = "SELECT id FROM mrt WHERE name = %s"
    category_id_query = "SELECT id FROM category WHERE name = %s"
    mrt_id = execute_query_read(mrt_id_query, (mrt_name,))[0]['id']
    category_id = execute_query_read(category_id_query, (category_name,))[0]['id']
    
    # Insert sight
    sight_query = "INSERT INTO sight (id, name, description, address, transport, lat, lng, mrt_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    execute_query_update(sight_query, (id, name, description, address, transport, lat, lng, mrt_id, category_id))
    
    # Get sight ID
    sight_id_query = "SELECT id FROM sight WHERE name = %s"
    sight_id = execute_query_read(sight_id_query, (name,))[0]['id']
    
    # Extract JPG URLs
    jpg_urls = extract_jpg_urls(entry['file'])
    
    # Insert file URLs
    for jpg_url in jpg_urls:
        file_query = "INSERT INTO file (sight_id, url) VALUES (%s, %s)"
        execute_query_update(file_query, (sight_id, jpg_url))
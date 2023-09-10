import json, sys, re

sys.stdout.reconfigure(encoding='utf-8')

import mysql.connector.pooling


# probe SQL data for translation replacement

# Configuration for the database connection pool
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "MyNewPass5!",
    "database": "mydb",
}

# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

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
    

query = "SELECT id, name FROM sight"
query_result = execute_query_read(query)

dict_newform = {}

for item in query_result:
    dict_newform[item['id']] = item['name']
    
print(dict_newform)
    
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
        
mrt_english = {
    20: 'No MRT Station!', 
    18: 'Zhongshan', 
    10: 'Chiang Kai-Shek Memorial Hall', 
    33: 'Gongguan', 
    4: 'Jiantan', 
    12: 'Taipei Zoo', 
    29: 'Beitou', 
    16: 'Taipei 101 / World Trade Center', 
    5: 'Qilian', 
    19: 'Sun Yat-Sen Memorial Hall', 
    22: 'Yuanshan', 
    3: 'Shilin', 
    6: 'Daan Park', 
    23: 'Dahu Park', 
    24: 'Dazhi', 
    11: 'Taipei City Hall', 
    14: 'Zhongxiao Xinsheng', 
    26: 'Zhongyi', 
    21: 'Wende', 
    1: 'Xinbeitou', 
    31: 'Muzha', 
    28: 'Songshan', 
    17: 'Songjiang Nanjing', 
    25: 'Shipai', 
    15: 'National Taiwan University Hospital', 
    32: 'Zhishan', 
    30: 'Huzhou', 
    9: 'Xingtian Temple', 
    27: 'Ximen', 
    7: 'Xiangshan', 
    13: 'Guandu', 
    2: 'Shuanglian', 
    8: 'Longshan Temple',
}

category_eng = {
  8: 'Others',
  5: 'Cycling',
  7: 'Religion',
  6: 'Outdoor Activity',
  3: 'Historic Building',
  2: 'Boating',
  4: 'Cultural Center',
  9: 'Family Outings',
  1: 'Hot Springs',
}

def update_table_name(id):
    query = "UPDATE category SET name = %s WHERE id = %s"
    data = (category_eng[id], id)
    return execute_query_update(query, data)

# update_table_name(1)

# for item in range(2, 10):
#     update_table_name(item)

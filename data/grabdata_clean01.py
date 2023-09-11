import sys
# Set standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import json

# Load data from the JSON file
with open(r'C:\phase2\taipei-day-trip\data\taipei_travel_data_ch.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize an empty dictionary to store the processed data
processed_data = {}
data_reverse = {}

# Iterate through the list of attractions
for attraction in data:
    # Get the 'id' and 'name' fields
    attraction_id = attraction['id']
    attraction_name = attraction['name']

    # Add the data to the processed_data dictionary
    processed_data[attraction_id] = attraction_name
    data_reverse[attraction_name] = attraction_id
    

# Print the processed data
print(processed_data) # ['光點臺北']
# print(data_reverse['光點臺北'], end='', flush=True, file=sys.stdout, encoding='utf-8')

# 艋舺龍山寺
# search_target = input("please input a sight name!")

for item in range(5):
    print(item)

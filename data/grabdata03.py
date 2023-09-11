
import sys
# Set standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import requests
import json

url = "https://www.travel.taipei/open-api/zh-tw/attractions/all"
headers = {"Accept": "application/json"}

total_pages = 15  # Assuming there are 15 pages (424 / 30 = 14 with some remainder)

all_data = []

for page in range(1, total_pages + 1):
    params = {"page": page}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        all_data.extend(data['data'])  # Extend the list with 'data' from the response
    else:
        print(f"Error: Unable to fetch data for page {page}. Status code: {response.status_code}")

# Save all_data to a JSON file
with open('taipei_travel_data.json', 'w', encoding='utf-8') as file:
    json.dump(all_data, file, ensure_ascii=False, indent=4)

print(f"Data saved to taipei_travel_data.json")

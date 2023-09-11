import sys
# Set standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import requests

url = "https://www.travel.taipei/open-api/zh-tw/attractions/all"
headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Now 'data' contains the JSON response from the API
    # You can process it as needed
else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")

print(data['data'][2]['name'])
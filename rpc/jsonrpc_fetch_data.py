import json
import random
import requests
import os

server_url = 'http://localhost:1769'
db_name = 'v17e_test'
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

json_endpoint = "%s/jsonrpc" % server_url
headers = {"Content-Type": "application/json"}

def get_json_payload(service, method, *args):
    return json.dumps({
        "jsonrpc": "2.0",
        "method": 'call',
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": random.randint(0, 1000000000),
    })
    
payload = get_json_payload("common", "login", db_name, username, password)
response = requests.post(json_endpoint, data=payload, headers=headers)
user_id = response.json()['result']

if user_id:
    # search for the room's ids
    search_domain = [['room_name', 'ilike', 'Hostel']]
    payload = get_json_payload("object", "execute_kw",
        db_name, user_id, password,
        'hostel.room', 'search', [search_domain], {'limit': 5})
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print('Search Result:', res)  # ids will be in result keys

    # read data for rooms ids
    payload = get_json_payload("object", "execute_kw",
        db_name, user_id, password,
        'hostel.room', 'read', [res['result'], ['room_name', 'room_number']])
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print('Rooms data:', res)
else:
    print("Failed: wrong credentials")
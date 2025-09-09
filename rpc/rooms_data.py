from xmlrpc import client
import os

# room data with search method
server_url = 'http://localhost:1769'
db_name = 'v17e_test'
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    search_domain = [['room_name', 'ilike', 'New']]
    # rooms_ids = models.execute_kw(db_name, user_id, password,
    #     'hostel.room', 'search',
    #     [search_domain],
    #     {'limit': 5})
    # print('Rooms ids found:', rooms_ids)

    # rooms_data = models.execute_kw(db_name, user_id, password,
    #     'hostel.room', 'read',
    #     [rooms_ids, ['room_name', 'room_number']])
    # print("Rooms data:", rooms_data)
    
    rooms_ids = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'search_read',
        [search_domain, ['room_name', 'room_number', 'state']],
        {'limit': 5})
    print('Rooms data:', rooms_ids)

else:
    print('Wrong credentials')
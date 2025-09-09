from xmlrpc import client
import os

server_url = 'http://localhost:1769'
db_name = 'v17e_test'
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    # Create room with state draft
    room_id = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'create',
        [{
            'room_name': 'New Room',
            'room_number': '35',
            'state': 'draft'
        }])
    # Call make_available method on new room
    print('Room created with id:', room_id)
    models.execute_kw(db_name, user_id, password,
        'hostel.room', 'make_available',
        [[room_id]])

    # check room status after method call
    room_data = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'read',
        [[room_id], ['room_name', 'state']])
    print('Room state after method call:', room_data[0]['state'])
else:
    print('Wrong credentials')
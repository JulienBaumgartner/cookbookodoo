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
    # create new room records.
    create_data = [
        {'room_name': 'Room 1', 'room_number': '101'},
        {'room_name': 'Room 3', 'room_number': '102'},
        {'room_name': 'Room 5', 'room_number': '103'},
        {'room_name': 'Room 7', 'room_number': '104'}
    ]
    rooms_ids = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'create',
        [create_data])
    print("Rooms created:", rooms_ids)

    # Write in existing room record
    room_to_write = rooms_ids[1]  # We will use ids of recently created rooms
    write_data = {'room_name': 'Room 2'}
    written = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'write',
        [room_to_write, write_data])
    print("Rooms written", written)

    # Delete the room record
    rooms_to_delete = rooms_ids[2:]
    deleted = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'unlink',
        [rooms_to_delete])
    print('Rooms unlinked:', deleted)

else:
    print('Wrong credentials')
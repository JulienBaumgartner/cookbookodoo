import odoorpc
import os

db_name = 'v17e_test'
user_name = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=1769)
odoo.login(db_name, user_name, password)  # login

# User information
user = odoo.env.user
print(user.name)             # name of the user connected
print(user.company_id.name)  # the name of user's company
print(user.email)            # the email of usser

RoomModel = odoo.env['hostel.room']
search_domain = [['room_name', 'ilike', 'Hostel']]
rooms_ids = RoomModel.search(search_domain, limit=5)
for room in RoomModel.browse(rooms_ids):
    print(room.room_name, room.room_number)

# create the room and update the state
room_id = RoomModel.create({
    'room_name': 'Test Room',
    'room_number': '37',
    'state': 'draft'
})
print("Room state before make_available:", room.state)
room = RoomModel.browse(room_id)
room.make_available()
room = RoomModel.browse(room_id)
print("Room state after make_available:", room.state)
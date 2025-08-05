from . import models
from . import controllers
from . import wizards

from odoo import api, SUPERUSER_ID

def add_room_hook(env):
    room_data1 = {'room_name': 'Room hook 1', 'room_number': '0001', 'room_floor': '1', 'student_per_room': '2'}
    room_data2 = {'room_name': 'Room hook 2', 'room_number': '0002', 'room_floor': '1', 'student_per_room': '2'}
    env['hostel.room'].create([room_data1, room_data2])
    
def pre_init_hook_hostel(env):
    print("Pre-init hook called")

def uninstall_hook_user(env):
    print("Uninstall hook called")
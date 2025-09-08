# -*- coding: utf-8 -*-

import logging
import random

from odoo import models
from odoo.tools import populate

_logger = logging.getLogger(__name__)


class RoomData(models.Model):
    _inherit = 'hostel.student'
    _populate_sizes = {'small': 10, 'medium': 100, 'large': 500}
    _populate_dependencies = ["res.partner"]

    def _populate_factories(self):
        partner_ids = self.env.registry.populated_models['res.partner']
        return [
            ('partner_id', populate.randomize(partner_ids)),
        ]

class HostelData(models.Model):
    _inherit = 'hostel.room'
    _populate_sizes = {'small': 10, 'medium': 100, 'large': 500}
    _populate_dependencies = ["hostel.student"]

    def _populate_factories(self):
        _logger.warning("Populate factory for hostel.room called!")
        student_ids = self.env.registry.populated_models['hostel.student']
        def get_student_ids(values, counter, random):
            return [
                (6, 0, [
                    random.choice(student_ids) for i in range(random.randint(1, 2))
                ])
            ]
        
        room_number_start = 10000
        def get_room_number(values, counter, random):
            room_number_start += 1
            return room_number_start
        
        return [
            ('room_name', populate.constant('Hostel Room {counter}')),
            ('room_number', populate.compute(get_room_number)),
            ('student_per_room', populate.randint(3, 4)),
            ('student_ids', populate.compute(get_student_ids)),
        ]
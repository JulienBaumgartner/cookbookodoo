from odoo import fields, models, api

class HostelRoom(models.Model):
    _name = 'hostel.room.stage'
    _order = 'sequence,name'
    
    name = fields.Char("Name")
    sequence = fields.Integer("Sequence")
    fold = fields.Boolean("Fold?")
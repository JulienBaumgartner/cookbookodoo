from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class HostelCategory(models.Model):
    _name = "hostel.categ"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hostel Category"
    _parent_store = True
    _parent_name = "parent_id" # optional if field is 'parent_id'
    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one('hostel.categ',string='Parent Category',ondelete='restrict',index=True)
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many('hostel.categ', 'parent_id',string='Child Categories')
    hostel_room_ids = fields.One2many(
        'hostel.room', 'category_id',
        string='Hostel Room')
    related_hostel_room = fields.Integer(compute='_compute_related_hostel_room')
    date_end = fields.Datetime(string='Ending Date', index=True, copy=False)
    date_assign = fields.Datetime(string='Assigning Date', copy=False,)
    address = fields.Char(string="Address")
    
    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
        
    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        
        record = self.env['hostel.categ'].create(parent_category_val)
        
        
    def _compute_related_hostel_room(self):
        for record in self:
            record.related_hostel_room = self.env['hostel.room'].search_count([
                ('category_id', '=', record.id),
            ])
        
    def action_open_related_hostel_room(self):
        related_hostel_room_ids = self.env['hostel.room'].search([
                ('category_id', '=', self.id),
            ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hostel Room'),
            'res_model': 'hostel.room',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_hostel_room_ids)],
        }
        
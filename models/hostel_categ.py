from odoo import models, fields, api
from odoo.exceptions import ValidationError
class HostelCategory(models.Model):
    _name = "hostel.categ"
    _description = "Hostel Category"
    _parent_store = True
    _parent_name = "parent_id" # optional if field is 'parent_id'
    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one('hostel.categ',string='Parent Category',ondelete='restrict',index=True)
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many('hostel.categ', 'parent_id',string='Child Categories')
    
    
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
        
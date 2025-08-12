from odoo import fields, models, api
class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Information about hostel"
    _order = "id desc, name"
    _rec_name = 'hostel_code'
    _rec_names_search = ['name', 'code']
    name = fields.Char(string="Hostel Name", required=True)
    hostel_code = fields.Char(string="Code", required=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one('res.country', string='Country')
    
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    hostel_floors = fields.Integer(string="Total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    type = fields.Selection([("male", "Boys"), ("female","Girls"), ("common", "Common")], "Type", help="Type of Hostel", required=True, default="common")
    other_info = fields.Text("Other Information", help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating', digits='Rating Value')
    category_id = fields.Many2one('hostel.categ', string='Category')
    ref_doc_id = fields.Reference(groups='my_hostel.group_hostel_manager', selection='_referencable_models', string='Reference Document')


    is_public = fields.Boolean(groups='my_hostel.group_hostel_manager')
    notes = fields.Text(groups='my_hostel.group_hostel_manager')
    date_start = fields.Date('Start Date', groups='my_hostel.group_start_date')

    @api.depends('hostel_code')
    def _compute_display_name(self): 
        for record in self:
            name = record.name
            if record.hostel_code:
                name = f'{name} ({record.hostel_code})'
            record.display_name = name
            
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]
            
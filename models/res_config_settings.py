from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_hostel_user = fields.Boolean(string="Hostel User", implied_group='my_hostel.group_hostel_user')
    group_start_date = fields.Boolean("Manage Hostel Start dates",group='base.group_user',
                                      implied_group='my_hostel.group_start_date')
    module_my_module = fields.Boolean("Install my_module")
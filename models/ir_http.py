from odoo import exceptions, http, models
from odoo.http import request

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'
    
    @classmethod
    def _auth_method_my_hostel_group_hostel_manager(cls):
        cls._auth_method_user()
        if not request.env.user.has_group('my_hostel.group_hostel_manager'):
            raise exceptions.AccessDenied()
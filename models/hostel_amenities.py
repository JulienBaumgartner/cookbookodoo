from odoo import fields, models
class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"
    _rec_name = 'name'
    name = fields.Char("Name", help="Provided Hostel Amenity")
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate whether the amenity should be given or not")

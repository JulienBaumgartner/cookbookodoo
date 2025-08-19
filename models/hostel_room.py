from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
from odoo.tests.common import Form
import logging
EXPORTS_DIR = '/srv/exports'
_logger = logging.getLogger(__name__)
class HostelRoom(models.Model):
    _name = "hostel.room"
    _inherit = ['base.archive', 'mail.thread', 'mail.activity.mixin']
    _description = "Hostel Room Information"
    _rec_name = 'room_name'
    _sql_constraints = [("room_number_unique", "unique(room_number)", "Room number must be unique!")]
    
    @api.model
    def _default_room_stage(self):
        stage = self.env['hostel.room.stage']
        return stage.search([], limit=1)
    
    @api.model
    def _group_expand_stages(self, stages, domain, order):
        return stages.search([], order=order)
    
    active = fields.Boolean(default=True)
    room_name = fields.Char(string="Room Name", required=True)
    room_number = fields.Integer(string="Room Number", required=True)
    room_floor = fields.Integer(string="Room Floor", required=True)
    description = fields.Html('Description')
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month") # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'
    student_per_room = fields.Integer("Student Per Room", required=True, default=1, help="Students allocated per room")
    
    availability = fields.Float(compute="_compute_check_availability", store=True, string="Availability", help="Room availability in hostel")
    
    hostel_id = fields.Many2one("hostel.hostel", "Hostel", help="Name of hostel")
    student_ids = fields.One2many("hostel.student", "room_id", string="Students", help="Enter students")
    hostel_amenities_ids = fields.Many2many("hostel.amenities", "hostel_room_amenities_rel", "room_id", "amenity_id", string="Amenities", domain="[('active', '=', True)]", help="Select hostel room amenities")

    # state = fields.Selection([('draft', 'Unavailable'),('available', 'Available'),('closed', 'Closed')],'State', default="draft")
    stage_id = fields.Many2one('hostel.room.stage', string='Stage', default=_default_room_stage, group_expand="_group_expand_stages")
    remarks = fields.Text('Remarks')
    previous_room = fields.Many2one('hostel.room', string='Previous Room')
    category_id = fields.Many2one('hostel.categ', string='Category')
    allocation_date = fields.Date(string="Allocation Date")
    room_rating = fields.Float('Hostel Average Rating', digits=(14, 4))
    sequence = fields.Integer(default=10)
    other_info = fields.Text("Other Information",
        help="Enter more information")
    related_students = fields.Integer(compute='_compute_related_students')
    
    color = fields.Integer()
    popularity = fields.Selection([('no', 'No Demand'), ('low','Low Demand'),
                                   ('medium', 'Average Demand'), ('high', 'High Demand'),])
    

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))
        
    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)
            
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),('available', 'closed'),('closed', 'draft')]
        return (old_state, new_state) in allowed
    
    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)
    
    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')

    def log_all_room_members(self):
        # This is an empty recordset of model hostel.student
        hostel_student_obj = self.env['hostel.student']
        all_members = hostel_student_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True
    
    def find_room(self):
        domain = [
            ('hostel_id.name', 'ilike', 'Hotel AAA')
        ]
        rooms = self.search(domain)
        domain2 = [
            '|',
                '&', ('room_name', 'ilike', 'Budget'),
                     ('hostel_id.name', 'ilike', 'Hotel AAA'),
                '&', ('room_name', 'ilike', 'Free'),
                    ('hostel_id.name', 'ilike', 'BBB')
        ]
        rooms2 = self.search(domain2)
        print("Rooms:", rooms & rooms2)
        
    def find_partner(self):
        PartnerObj = self.env['res.partner']
        domain = [
            '&', ('name', 'ilike', 'Azure Interior'),
            ('city', '=', 'Fremont')
        ]   
        partner = PartnerObj.search(domain)
        print("Partner:", partner)
        
    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        #print("Filtered rooms:", filtered_rooms)
        print("Filtered rooms:", self.get_students_names(filtered_rooms))
        
    @api.model
    def rooms_with_multiple_members(self, all_rooms):  
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
        #return all_rooms.filtered(predicate)
        return all_rooms.filtered(lambda b: len(b.student_ids) > 1)
    
    @api.model
    def get_students_names(self, rooms):
        return rooms.mapped('student_ids.name')
    
    def show_result(self):
        all_rooms = self.search([])
        print("Sort by rent:", self.sort_rooms_by_rent(all_rooms))
    
    
    @api.model
    def sort_rooms_by_rent(self, rooms):
        return rooms.sorted(key='rent_amount', reverse=True)

    @api.model
    def create(self, values):
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
        )
        return super(HostelRoom, self).create(values)
    
    def write(self, values):
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
                )
        return super(HostelRoom, self).write(values)

    def name_get(self):
        result = []
        for room in self:
            member = room.member_ids.mapped('name')
            name = '%s (%s)' % (room.name, ', '.join(member))
            result.append((room.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args += ['|', '|',
                      ('room_name', operator, name),
                      ('room_number', operator, name),
                      ('student_ids.name', operator, name)
                      ]
        return super(HostelRoom, self).name_search(
            name='', args=args, operator=operator,
            limit=limit)

    @api.model
    def get_average_cost(self, values):
        grouped_result = self.read_group(
            [('rent_amount', "!=", False)],  # Domain
            ['category_id', 'rent_amount:avg'],  # Fields to access
            ['category_id']  # group_by
        )
        return grouped_result

    @api.model
    def _update_room_price(self):
        all_rooms = self.search([])
        for room in all_rooms:
            room.rent_amount += 10

    @api.model
    def update_room_price(self, category_id, amount_to_increase):
        category_rooms = self.search([('category_id', '=', category_id)])
        for room in category_rooms:
            room.rent_amount += amount_to_increase
            
    @api.model
    def log_room_details(self,  values):
        all_rooms = self.search([])
        _logger.info("Logging rooms details:")
        for room in all_rooms:
            _logger.info("Room Name: %s, Room Number: %s, Rent Amount: %s",
                         room.room_name, room.room_number, room.rent_amount)
        return True
    
    def action_remove_room_members(self):
        for student in self.student_ids:
            student.with_context(is_hostel_room=True).action_remove_room()
    
    def action_category_with_amount(self):
        self.env.cr.execute("""
                            SELECT
                            hrc.name,
                            hostel_room.room_name
                            FROM
                            hostel_room AS hostel_room
                            JOIN
                            hostel_categ as hrc ON hrc.id = hostel_room.category_id
                            WHERE hostel_room.category_id = %(cate_id)s;""",
                            {'cate_id': self.category_id.id})
        result = self.env.cr.fetchall()
        _logger.info("Hostel Room With Amount: %s", result)
        
    def _compute_related_students(self):
        for record in self:
            record.related_students = self.env['hostel.student'].search_count([
                ('room_id', '=', record.id),
            ])
        
    def action_open_related_students(self):
        related_students_ids = self.env['hostel.student'].search([
                ('room_id', '=', self.id),
            ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hostel Students'),
            'res_model': 'hostel.student',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_students_ids)],
        }
    

    
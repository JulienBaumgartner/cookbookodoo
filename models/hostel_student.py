from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
from odoo.tests.common import Form
from datetime import timedelta
class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = "Hostel Student Information"
    _rec_name = 'name'
    partner_id = fields.Many2one('res.partner', ondelete='cascade', delegate=True)
    gender = fields.Selection([("male", "Male"),("female", "Female"), ("other", "Other")],string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    room_id = fields.Many2one("hostel.room", "Room", help="Select hostel room")
    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')
    admission_date = fields.Date("Admission Date", help="Date of admission in hostel", default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date", help="Date on which student discharge")
    # duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration", help="Enter duration of living")
    # duration = fields.Integer("Duration", help="Enter duration of living")
    duration = fields.Integer("Duration", compute="onchange_duration", help="Enter duration of living")
    room_no = fields.Char('Room No')
    status = fields.Selection([("draft", "Draft"),
                    ("reservation", "Reservation"), ("pending", "Pending"),
                    ("paid", "Done"),("discharge", "Discharge"), ("cancel", "Cancel")],
                    string="Status", copy=False, default="draft",
                    help="State of the student hostel")
    
    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Method to check duration"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days
                
    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')

    def update_room_no(self):
        self.ensure_one()
        self.room_no = "RM002"


    def action_assign_room(self):
        self.ensure_one()
        if self.status != "paid":
            raise UserError(_("You can't assign a room if it's not paid."))
        room_as_superuser = self.env['hostel.room'].sudo()
        room_rec = room_as_superuser.create({
        "room_name": "Room A-103",
        "room_number": "1234",
        "room_floor": 1,
        "student_per_room": 1,
        })
        if room_rec:
            self.room_id = room_rec.id
            
    def action_assign_room_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign Room'),
            'res_model': 'assign.room.student.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'new',
        }

    def action_remove_room(self):
        if self.env.context.get("is_hostel_room"):
            self.room_id = False
        else:
            raise UserError(_("You can only remove the room from the student record in the hostel room context."))

    #@api.onchange('admission_date', 'discharge_date') #coté client uniquement
    @api.depends('admission_date', 'discharge_date')
    def onchange_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                stu.duration = (stu.discharge_date.year - stu.admission_date.year) * 12 + (stu.discharge_date.month - stu.admission_date.month)

    def return_room(self):
        self.ensure_one()
        wizard = self.env['assign.room.student.wizard']
        with Form(wizard) as return_form:
            return_form.room_id = self.env.ref('my_hostel.hostel_room_404')
            record = return_form.save()
            record.with_context(active_id=self.id).add_room_in_student()

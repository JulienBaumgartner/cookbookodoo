from odoo import http, fields
from odoo.http import request
import email
import datetime

class Main(http.Controller):
    @http.route('/my_hostel/students', type='http', auth='none')
    def students(self):
        students = request.env['hostel.student'].sudo().search([])
        html_result = '<html><body><ul>'
        for student in students:
            html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return request.make_response(
            html_result, headers=[
                ('Last-modified', email.utils.formatdate(
                    (
                        fields.Datetime.from_string(
                            request.env['hostel.student'].sudo()
                            .search([], order='write_date desc', limit=1)
                            .write_date) -
                        datetime.datetime(1970, 1, 1)
                    ).total_seconds(),
                    usegmt=True)),
            ])

    @http.route('/my_hostel/students/json', type='json', auth='none')
    def students_json(self):
        records = request.env['hostel.student'].sudo().search([])
        return records.read(['name'])

    @http.route('/my_hostel/all-students', type='http', auth='none')
    def all_students(self):
        students = request.env['hostel.student'].sudo().search([])
        html_result = '<html><body><ul>'
        for student in students:
            html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return html_result
    
    @http.route('/my_hostel/all-students/mark-mine', type='http', auth='public')
    def all_students_mark_mine(self):
        students = request.env['hostel.student'].sudo().search([])
        hostels = request.env['hostel.hostel'].sudo().search([('rector', '=', request.env.user.partner_id.id)])
        hostel_rooms = request.env['hostel.room'].sudo().search([('hostel_id', 'in', hostels.ids)])
        html_result = '<html><body><ul>'
        for student in students:
            if student.id in hostel_rooms.student_ids.ids:
                html_result += "<li> <b>%s</b> </li>" % student.name
            else:
                html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return html_result
    
    @http.route('/my_hostel/all-students/mine', type='http', auth='user')
    def all_students_mine(self):
        hostels = request.env['hostel.hostel'].sudo().search([('rector', '=', request.env.user.partner_id.id)])
        students = request.env['hostel.room'].sudo().search([('hostel_id', 'in', hostels.ids)]).student_ids
        html_result = '<html><body><ul>'
        for student in students:
            html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return html_result
    
    @http.route('/my_hostel/manager', type='http', auth='my_hostel_group_hostel_manager')
    def manager(self):
        html_result = '<html><body>ok</body></html>'
        return html_result
    
    @http.route('/my_hostel/student_details', type='http', auth='none')
    def student_details(self, student_id):
        record = request.env['hostel.student'].sudo().browse(int(student_id))
        return u'<html><body><h1>%s</h1>Room No: %s' % (
            record.name, str(record.room_id.room_number) or 'none')

    @http.route("/my_hostel/student_details/<model('hostel.student'):student>",
                type='http', auth='none')
    def student_details_in_path(self, student):
        return self.student_details(student.id)
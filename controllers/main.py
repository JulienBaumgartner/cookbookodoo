from odoo import http, fields
from odoo.http import request
import email
import datetime
from odoo.addons.website.controllers.main import Website
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
import werkzeug

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
    
    @http.route('/demo_page', type='http', auth='none')
    def students_img(self):
        image_url = '/my_hostel/static/src/img/icon.png'
        html_result = """<html>
                         <body>
                         <img src="%s"/>
                         </body>
                        </html>""" % image_url
        return html_result
    
    @http.route('/custom-page', type='http', auth='public', website=True)
    def custom_page(self, **kw):
        return request.render('my_hostel.custom_template', {})


    def sitemap_hostels(env, rule, qs):
        Hostels = env['hostel.hostel']
        dom = sitemap_qs2dom(qs, '/hostels', Hostels._rec_name)
        #Ex. to filter urls
        #dom += [('name', 'ilike', 'abc')]
        for f in Hostels.search(dom):
            loc = '/hostels/%s' % slug(f)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route('/hostel/<model("hostel.hostel"):hostel>',
                type='http', auth="public", website=True, sitemap=sitemap_hostels)
    def hostel_room_detail(self, hostel, **post):
        if not hostel.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()
        return request.render(
            'my_hostel.hostel_detail', {
            'hostel': hostel,
            'main_object': hostel
            })

    @http.route('/my_hostel/all-hostels', type='http', auth='public')
    def all_hostels(self):
        hostels = request.env['hostel.hostel'].sudo().search([])
        html_result = '<html><body><ul>'
        for hostel in hostels:
            html_result += "<li> %s <a href='/hostel/%d'>View Details</a></li>" % (hostel.name, hostel.id)
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/my_hostel/hostelsJson/<int:limit>', type='json', auth='public', website=True)
    def get_values(self, limit, **post):
        
        country_id = False
        country_ids = False
        country_code = request.geoip and request.geoip.get('country_code') or 'CH'
        if country_code:
            country_ids = request.env['res.country'].sudo().search([('code', '=', country_code)])
        if country_ids:
            country_id = country_ids[0].id
        domain = ['|', ('restrict_country_ids', '=', False), ('restrict_country_ids', 'not in', [country_id])]
        
        domain += request.website.website_domain()
        
        records = request.env['hostel.hostel'].sudo().search(domain, limit=limit)
        return [{'id': r.id, 'name': r.name, 'hostel_code': r.hostel_code} for r in records]
    
    

class WebsiteInfo(Website):
    @http.route()
    def website_info(self):
        result = super(WebsiteInfo, self).website_info()
        result.qcontext['apps'] = result.qcontext['apps'].filtered(
            lambda x: x.name != 'website'
        )
        return result
    
class InquiryForm(http.Controller):
    @http.route('/inquiry/form', type='http', auth="public",
                website=True)
    def inquiry_form_template(self, **kw):
        return request.render("my_hostel.hostel_inquiry_form")

    @http.route('/inquiry/submit', type='http', auth="public",
                website=True)
    def inquiry_form(self, **kwargs):
        inquiry_obj = request.env['hostel.inquiries']
        form_vals = {
            'name': kwargs.get('name') or '',
            'email': kwargs.get('email') or '',
            'phone': kwargs.get('phone') or '',
            'book_fy': kwargs.get('book_fy') or '',
            'queries': kwargs.get('queries') or '',
            }
        submit_success = inquiry_obj.sudo().create(form_vals)
        return request.redirect('/contactus-thank-you')
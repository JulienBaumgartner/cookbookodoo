from odoo.tests.common import TransactionCase, tagged

@tagged('-at_install', 'post_install')
class TestHostelRoomState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestHostelRoomState, self).setUp(*args, **kwargs)
        self.partner_nikul = self.env['res.partner'].create({'name': 'Nikul Chaudhary'})
        self.partner_deepak = self.env['res.partner'].create({'name': 'Deepak Ahir'})
        self.member_ids = self.env['hostel.student'].create([
            {'partner_id': self.partner_nikul.id, 'room_no': '007'},
            {'partner_id': self.partner_deepak.id, 'room_no': '357'}])
        self.test_hostel_room = self.env['hostel.room'].create({
            'room_name': 'TestHostelRoomState',
            'room_number': '10000',
            'room_floor': '1',
            'student_per_room': '2',
            'student_ids': [(6, 0, self.member_ids.ids)]
        })

    def test_button_available(self):
        """Make available button"""
        self.test_hostel_room.make_available()
        self.assertIn(self.partner_nikul, self.test_hostel_room.mapped('student_ids.partner_id'))
        self.assertEqual(
            self.test_hostel_room.state, 'available', 'Hostel Room state should changed to available')

    def test_button_closed(self):
        """Make closed button"""
        self.test_hostel_room.make_available()
        self.test_hostel_room.make_closed()
        self.assertEqual(
            self.test_hostel_room.state, 'closed', 'Hostel Room state should changed to closed')
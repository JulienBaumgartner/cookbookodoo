from odoo.tests.common import TransactionCase, tagged
from odoo.tests import HttpCase

@tagged('post_install', '-at_install')
class TestUi(HttpCase):
    def test_01_hostel_tour(self):
        self.start_tour("/web", 'hostel_test_tour', login="admin")
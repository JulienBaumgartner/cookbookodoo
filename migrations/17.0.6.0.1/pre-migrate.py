def migrate(cr, version):
    cr.execute('ALTER TABLE hostel_room RENAME COLUMN allocation_date TO allocation_date_char')
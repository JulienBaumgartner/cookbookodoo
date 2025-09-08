/** @odoo-module **/
import { getFixture } from "@web/../tests/helpers/utils";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";

QUnit.module('IntColorField Tests', {}, function() {

    QUnit.module("Fields");

    QUnit.test('render color field', async function (assert) {
        assert.expect(1);
        let target = getFixture();
        setupViewRegistries();

        await makeView({
            type: "form",
            resModel: "hostel.room",
            serverData: {
                models: {
                    'hostel.room': {
                        fields: {
                            room_name: { string: "Room Name", type: "char" },
                            room_number: { string: "Room Number", type: "char" },
                            color2: { string: "color", type: "integer"},
                        },
                        records: [
                            {
                                id: 1,
                                room_name: "Hostel Room 01",
                                room_number: 1,
                                color2: 1,
                            },
                            {
                                id: 2,
                                room_name: "Hostel Room 02",
                                room_number: 2,
                                color2: 3
                            }
                        ],
                    },
                },
                views: { },
            },
            arch: `
            <form>
                <field name="room_name"/>
                <field name="room_number"/>
                <field name="color2" widget="int_color"/>
            </form>`,
        });
        assert.containsN(
            target,
            ".o_field_int_color",
            1,
            "Both records are rendered"
        );
    });
});
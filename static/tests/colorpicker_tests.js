/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { uiService } from "@web/core/ui/ui_service";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";
import { click, getFixture, patchWithCleanup } from "@web/../tests/helpers/utils";

const serviceRegistry = registry.category("services");

QUnit.module("Color Picker Widget Tests", (hooks) => {
    let serverData;
    let target;
    hooks.beforeEach(async function (assert) {
        target = getFixture();
        serverData = {
            models: {
                'hostel.room': {
                    fields: {
                        room_name: { string: "Hostel Name", type: "char" },
                        room_number: { string: "Room Number", type: "char" },
                        color2: { string: "color2", type: "integer" },
                    },
                    records: [{
                        id: 1,
                        room_name: "Hostel Room 01",
                        room_number: 10001,
                        color2: 1,
                    }, {
                        id: 2,
                        room_name: "Hostel Room 02",
                        room_number: 10002,
                        color2: 3
                    }],
                },
            },
            views: {
                "hostel.room,false,form": `<form>
                    <field name="room_name"/>
                    <field name="room_number"/>
                    <field name="color2" widget="custom_color"/>
                </form>`,
            },
        };
        serviceRegistry.add("ui", uiService);
        setupViewRegistries();
    });

    QUnit.module("OWLCategColorField");

    QUnit.test("factor is applied in OWLCategColorField", async function (assert) {
        const form = await makeView({
            serverData,
            type: "form",
            resModel: "hostel.room",
        });

        assert.containsOnce(target, '.o_field_custom_color');

        assert.strictEqual(target.querySelectorAll(".o_field_custom_color .o_color_pill").length, 6, "Color picker should have 6 pills");

        await click(target.querySelectorAll(".o_field_custom_color .o_color_pill")[3]);

        assert.strictEqual(target.querySelector('.o_field_custom_color .o_color_4').classList.contains("active"), true, "Click on pill should make pill active");
    });

    hooks.afterEach(() => {
        const extra = document.querySelector(".bg-info.text-white");
        if (extra) {
            extra.remove();
        }
    });

});
/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_service/tour_utils";
import { markup } from "@odoo/owl";


registry.category("web_tour.tours").add("hostel_test_tour", {
    url: "/web",
    rainbowMan: false,
    sequence: 20,
    steps: () => [stepUtils.showAppsMenuItem(), {
        trigger: '.o_app[data-menu-xmlid="my_hostel.hostel_main_menu"]',
        content: markup(_t("Ready to launch your <b>Hostel</b>?")),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: '.o_app[data-menu-xmlid="my_hostel.hostel_main_menu"]',
        content: markup(_t("Ready to launch your <b>Hostel</b>?")),
        position: 'bottom',
        edition: 'enterprise',
    }, {
        trigger: '.o_list_button_add',
        content: markup(_t("Let's create new room.")),
        position: 'bottom',
    }, {
        trigger: ".o_form_view .o_field_char[name='name']",
        content: markup(_t('Add a new <b> Hostel Room </b>.')),
        position: "top",
        run: function (actions) {
            actions.text("Hostel Room 01", this.$anchor.find("input"));
        },
    }, {
        trigger: ".o_form_button_cancel",
        content: _t("Cancel the form"),
        position: "bottom",
        run: "click",
    }],
});
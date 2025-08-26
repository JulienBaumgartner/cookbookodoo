/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";

export async function getHostelsDB(limit) {
    try {
        const response = await fetch(`/my_hostel/hostelsJson/${limit}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        });

        if (!response.ok) {
            throw new Error("Erreur HTTP " + response.status);
        }

        const result = await response.json();
        console.log("Données récupérées :", result);
        return result;
    } catch (error) {
        console.error("Erreur RPC :", error);
        return [];
    }
}

publicWidget.registry.HostelSnippet = publicWidget.Widget.extend({
    selector: '.hostel_snippet',
    disabledInEditableMode: false,

    start: function () {
        var self = this;
        var rows = this.$el[0].dataset.numberOfHostels || '5';
        this.$el.find('td').parents('tr').remove();

        getHostelsDB(rows).then(data => {
            // data = { jsonrpc, id, result: [...] }
            const records = data.result || [];

            // Nettoyage de l'ancien contenu
            self.$el.find("tr").remove();

            // Ajout des nouvelles lignes
            records.forEach(hostel => {
                self.$el.append(
                    $("<tr />").append(
                        $("<td />").text(hostel.name),
                        $("<td />").text(hostel.hostel_code || ""),
                        $("<td />").html(`<a href='/hostel/${hostel.id}'>View Details</a>`),
                    )
                );
            });
        });
    },
});
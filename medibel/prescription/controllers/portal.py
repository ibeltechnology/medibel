from collections import OrderedDict
from werkzeug.exceptions import NotFound
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo import _, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager,
)



class PortalPrescription(CustomerPortal):

    # ---------------------------------------------------------
    # Domains
    # ---------------------------------------------------------

    def _prepare_prescriptions_domain(self, partner):
        return [
            ("patient_id", "=", partner.id),
            ("active", "=", True),
        ]

    # ---------------------------------------------------------
    # Counters
    # ---------------------------------------------------------

    def _prepare_portal_counter_values(self, counter):

        if counter == "prescription_count":

            partner = request.env.user.partner_id

            return (
                "prescription.order",
                self._prepare_prescriptions_domain(partner),
                "read",
            )

        return super()._prepare_portal_counter_values(counter)

    # ---------------------------------------------------------
    # Searchbar
    # ---------------------------------------------------------

    def _get_prescription_searchbar_sortings(self):
        return {
            "date": {
                "label": _("Date"),
                "order": "prescription_date desc, id desc",
            },
            "name": {
                "label": _("Reference"),
                "order": "name asc, id asc",
            },
        }

    def _get_prescription_searchbar_filters(self):
        return {
            "all": {
                "label": _("All"),
                "domain": [],
            },
        }

    # ---------------------------------------------------------
    # List
    # ---------------------------------------------------------

    @http.route(
        [
            "/my/prescriptions",
            "/my/prescriptions/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
        methods=["GET"],
    )
    def portal_my_prescriptions(
        self,
        page=1,
        sortby="date",
        filterby="all",
        **kw,
    ):

        values = self._prepare_portal_layout_values()

        Prescription = request.env["prescription.order"]

        if not Prescription.has_access("read"):
            raise NotFound()

        partner = request.env.user.partner_id

        domain = self._prepare_prescriptions_domain(partner)

        searchbar_sortings = (
            self._get_prescription_searchbar_sortings()
        )

        searchbar_filters = (
            self._get_prescription_searchbar_filters()
        )

        if sortby not in searchbar_sortings:
            sortby = "date"

        if filterby not in searchbar_filters:
            filterby = "all"

        order = searchbar_sortings[sortby]["order"]

        domain += searchbar_filters[filterby]["domain"]

        prescription_count = Prescription.search_count(domain)

        pager = portal_pager(
            url="/my/prescriptions",
            url_args={
                "sortby": sortby,
                "filterby": filterby,
            },
            total=prescription_count,
            page=page,
            step=self._items_per_page,
        )

        prescriptions = Prescription.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )

        request.session["my_prescriptions_history"] = (
            prescriptions.ids[:100]
        )

        values.update({
            "page_name": "prescription",
            "prescriptions": prescriptions,
            "pager": pager,
            "default_url": "/my/prescriptions",
            "searchbar_sortings": searchbar_sortings,
            "searchbar_filters": OrderedDict(
                sorted(searchbar_filters.items())
            ),
            "sortby": sortby,
            "filterby": filterby,
        })

        return request.render(
            "prescription.portal_my_prescriptions",
            values,
        )
    # ---------------------------------------------------------
    # Detail
    # ---------------------------------------------------------

    def _prescription_get_page_view_values(
        self,
        prescription,
        **kwargs,
    ):

        values = {
            "page_name": "prescription",
            "prescription": prescription,
        }

        return self._get_page_view_values(
            prescription,
            None,
            values,
            "my_prescriptions_history",
            False,
            **kwargs,
        )


# Méthodes à placer dans PortalPrescription(CustomerPortal)

    @http.route(
        ["/my/prescriptions/<int:prescription_id>"],
        type="http",
        auth="user",
        website=True,
        methods=["GET"],
        sitemap=False,
    )
    def portal_my_prescription_detail(
        self,
        prescription_id,
        report_type=None,
        download=False,
        **kw,
    ):
        Prescription = request.env["prescription.order"]
        partner = request.env.user.partner_id

        if not Prescription.has_access("read"):
            raise NotFound()

        # Le domaine doit être identique à celui de la liste.
        domain = list(self._prepare_prescriptions_domain(partner))
        domain.append(("id", "=", prescription_id))

        try:
            prescription = Prescription.search(domain, limit=1)

            if not prescription:
                raise NotFound()

            prescription.check_access("read")

            # Aperçu HTML ou téléchargement PDF.
            if report_type in ("html", "pdf"):
                response = self._show_report(
                    model=prescription,
                    report_type=report_type,
                    report_ref="prescription.prescription_order_report",
                    download=str(download).lower() in ("true", "1"),
                )

                # Les ordonnances contiennent des données médicales.
                response.headers["Cache-Control"] = (
                    "private, no-store, no-cache, max-age=0"
                )
                response.headers["Pragma"] = "no-cache"
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["X-Frame-Options"] = "SAMEORIGIN"
                response.headers["Content-Security-Policy"] = (
                    "frame-ancestors 'self'"
                )

                return response

            if report_type:
                raise NotFound()

            values = self._prepare_portal_layout_values()

            # Navigation sécurisée sans token de partage.
            history = request.session.get(
                "my_prescriptions_history", []
            )

            # On ne conserve que les identifiants encore accessibles.
            allowed_ids = Prescription.search([
                *self._prepare_prescriptions_domain(partner),
                ("id", "in", history),
            ]).ids

            allowed_set = set(allowed_ids)
            history = [
                record_id
                for record_id in history
                if record_id in allowed_set
            ]

            previous_url = False
            next_url = False

            if prescription.id in history:
                index = history.index(prescription.id)

                if index > 0:
                    previous_url = (
                        f"/my/prescriptions/{history[index - 1]}"
                    )

                if index < len(history) - 1:
                    next_url = (
                        f"/my/prescriptions/{history[index + 1]}"
                    )

            values.update({
                "page_name": "prescription",
                "prescription": prescription,
                "object": prescription,
                "message_per_page": 10,
                #"disable_composer": True,
                "prev_record": previous_url,
                "next_record": next_url,
                "no_breadcrumbs": False,
            })

            response = request.render(
                "prescription.portal_prescription_page",
                values,
            )

            response.headers["Cache-Control"] = (
                "private, no-store, no-cache, max-age=0"
            )
            response.headers["X-Frame-Options"] = "SAMEORIGIN"

            return response

        except (AccessError, MissingError):
            raise NotFound() from None

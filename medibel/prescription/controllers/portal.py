from collections import OrderedDict

from odoo import _, fields, http
from odoo.exceptions import AccessError, MissingError
from odoo.fields import Domain
from odoo.http import request
from odoo.tools import email_normalize, email_normalize_all
from odoo.tools.misc import verify_hash_signed

from odoo.addons.account.controllers.download_docs import _build_zip_from_data, _get_headers
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PortalAccount(CustomerPortal):

    def _prepare_portal_counter_values(self, counter):
        partner = self.env.user.partner_id
        if counter == 'prescription_count':
            return 'prescription.order', self._prepare_prescriptions_domain(partner), 'read'
        return super()._prepare_portal_counter_values(counter)

        
    def _prepare_prescriptions_domain(self, partner):
        return [
            ("patient_id", "child_of", [partner.commercial_partner_id.id]),
        ]

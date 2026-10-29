# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    prescription_count = fields.Integer(
        string='Prescriptions Count',
        compute='_compute_prescription_count'
    )


    def _compute_prescription_count(self):
        for record in self:
            record.prescription_count = self.env['prescription.order'].search_count([
                ('patient_id', '=', record.id)
            ])

    def action_view_prescription(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescriptions',
            'res_model': 'prescription.order',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id, 'create' : False},
        }

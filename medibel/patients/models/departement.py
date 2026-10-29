# -*- coding:utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Department(models.Model):
    _inherit = "departement.departement"

    patient_ids = fields.One2many('res.partner', 'departement_id', string='Patients')
    patient_ids_count = fields.Integer(compute="_compute_patient_ids",)

    def _compute_patient_ids(self):
        for record in self:
            record.patient_ids_count = self.env['patient.patient'].search_count([('is_patient', '=', True),('departement_id', '=', record.id)])
    def get_patient_ids_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'view_mode': 'list,form',
            'res_model': 'res.partner',
            'domain': [('departement_id', '=', self.id)],
            'context': {'create' : False}
        }


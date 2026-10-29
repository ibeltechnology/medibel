# -*- coding:utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Arrondissement(models.Model):
    _inherit = "arrondissement.arrondissement"

    patient_ids = fields.One2many('res.partner', 'arrondissement_id', string='Patients')
    patient_ids_count = fields.Integer(compute="_compute_patient_ids", string='', help='')

    def _compute_patient_ids(self):
        for record in self:
            record.patient_ids_count = self.env['res.partner'].search_count([('is_patient', '=', True),('arrondissement_id', '=', record.id)])
    def get_patient_ids_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'view_mode': 'list,form',
            'res_model': 'res.partner',
            'domain': [('arrondissement_id', '=', self.id)],
            'context': {'create' : False}
        }


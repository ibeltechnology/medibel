# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PrescriptionOrder(models.Model):
    _name = 'prescription.order'
    _description = 'prescription.order'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)
    prescription_date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    doctor_id = fields.Many2one(string='Prescribing physician', comodel_name='res.users', default=lambda self: self.env.user, readonly=True)
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner', domain="[('is_patient', '=', True)]")
    prescription_line_ids = fields.One2many(string='Prescription lines', comodel_name='prescription.line', inverse_name='prescription_id')
    notes = fields.Text(string='Notes')



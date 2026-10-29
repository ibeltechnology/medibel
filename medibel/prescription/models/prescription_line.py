# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class PrescriptionLine(models.Model):
    _name = 'prescription.line'
    _description = 'prescription.line'
    
    

    active = fields.Boolean(string='Actif', default=True)
    prescription_id = fields.Many2one('prescription.order','Prescription Order')
    medicament_id = fields.Many2one('product.template', string='Medicine', required=True, domain="[('is_medicament', '=', True)]")
    frequency_id = fields.Many2one('medication.frequency', string='Fequency', required=True)
    start_date = fields.Date(default=fields.Date.today(), string='Start of treatment')
    duration = fields.Float(digits=(6, 2), string="Duration of treatment (days)")
    end_date = fields.Date(string="Treatment end date", store=True, compute='_get_end_date', inverse='_set_end_date')
    short_comment = fields.Char('Comment', size=128 )
    
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            r.duration = (r.end_date - r.start_date).days + 1



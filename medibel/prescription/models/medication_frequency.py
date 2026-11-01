# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MedicationFrequency(models.Model):
    _name = 'medication.frequency'
    _description = 'medication.frequency'
    
    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)
    code = fields.Char(string='Code')
    abbreviation = fields.Char(string='Abbreviation')



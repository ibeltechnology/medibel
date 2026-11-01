# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MedicalGender(models.Model):
    _name = 'medical.gender'
    _description = 'medical.gender'
    
    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)



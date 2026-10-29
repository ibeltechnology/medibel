# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MedicamentDci(models.Model):
    _name = 'medicament.dci'
    _description = 'medicament.dci'
    
    

    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)



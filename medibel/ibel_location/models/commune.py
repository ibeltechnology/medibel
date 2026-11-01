# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Commune(models.Model):
    _name="commune.commune"
    _description = "Communes"

    name = fields.Char('Commune',required=True)   
    region_id = fields.Many2one('region.region', string="Région")
    departement_id = fields.Many2one('departement.departement',string="Département",)
    arrondissement_id = fields.Many2one( 'arrondissement.arrondissement', string="Arrondissement",)
    


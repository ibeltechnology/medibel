# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MedicalPathologyGroup(models.Model):
    _name = 'medical.pathology.group'
    _description = "Medical Pathology Group"
    
    name = fields.Char(string="Name",required=True)
    code = fields.Char(string="Code")
    desc = fields.Char(string="Short Description",required=True)
    info = fields.Text(string="Detailed Information")



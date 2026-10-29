# -*- coding:utf-8 -*-
#import
from odoo import models, fields, api, exceptions, _

class SpecialitySpeciality(models.Model):
    _name = "medical.specialty"
    _description = "medical.specialty"

    SPECIALITY_TYPE = [
          ("surgical","Surgical"),
          ("medical","Medical"),
          ]

    name = fields.Char(string='Name of the specialty')
    code = fields.Char(string='Code of the specialty')
    description = fields.Text(string='Description')
    specialty_type = fields.Selection(SPECIALITY_TYPE, string='Type')
    active = fields.Boolean('Active', default=True)


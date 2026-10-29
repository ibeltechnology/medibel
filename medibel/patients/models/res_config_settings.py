# -*- coding:utf-8 -*-
from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    module_icd11 = fields.Boolean(string='ICD 11')


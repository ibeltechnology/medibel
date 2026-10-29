# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dci_id = fields.Many2one(
        string='DCI',
        comodel_name='medicament.dci',
    )
    is_medicament = fields.Boolean(
        string='Is medicament'
    )

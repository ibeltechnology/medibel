
from odoo import models, fields, api, _

class MedicalPathology(models.Model):
    _name = 'medical.pathology'
    _description = "Medical Pathology"

    name = fields.Char(string="Name",required=True)
    code = fields.Char(string="Code")
    uri = fields.Char(string="URI")
    category_id = fields.Many2one('medical.pathology.category',string="Disease Category")
    is_genetic = fields.Boolean()
    line_ids = fields.One2many('medical.pathology.group.member','disease_group_id',string="Group")
    chromosome = fields.Char(string="Affected Chromosome")
    gene = fields.Char(string="Gene")
    protein = fields.Char(string="Protein")
    info = fields.Text(string="Extra Info")
    active = fields.Boolean(string='Active', default=True)

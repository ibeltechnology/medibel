from odoo import models, fields

class MedicalPathology(models.Model):
    _inherit = "medical.pathology"
    _description = "Extend medical pathology age range"

    age_range_ids = fields.Many2many('patient.age.range', string="Age range")

class PatientAgeRange(models.Model):
    _inherit = "patient.age.range"
    _description = "Extend age range pathology"

    pathology_ids = fields.Many2many("medical.pathology", string="Pathologies")
    

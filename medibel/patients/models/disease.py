# -*- coding:utf-8 -*-
from dateutil.relativedelta import relativedelta 
from odoo import models, fields, api, exceptions, _
class PatientDisease(models.Model):
    _name = "patient.disease"
    _description = "patient.disease"
    _rec_name = 'patient_id'

    pathology_id = fields.Many2one('medical.pathology','Pathology', required=True)
    diagnosis_date = fields.Date('Date of diagnosis')
    age = fields.Char('Age at diagnosis', compute="_compute_age_diagnosis")
    patient_id = fields.Many2one('res.partner',string="Patient", domain="[('is_patient', '=', True)]")
    doctor_id = fields.Many2one('res.partner',string="Doctor", domain="[('is_physician', '=', True)]")
    extra_info = fields.Text('infos complémentaires')
    active = fields.Boolean('Active', default=True)
    
    @api.depends('patient_id.date_of_birth', 'diagnosis_date')
    def _compute_age_diagnosis(self):
        for rec in self:
            if rec.patient_id.date_of_birth:
                d1 = rec.patient_id.date_of_birth
                d2 = rec.diagnosis_date
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + " year(s)" +" "+ str(rd.months) + " months" +" "+ str(rd.days) + " days"
            else:
                rec.age = "No date of birth!!"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Vérifie si l'utilisateur courant est un médecin
        if self.env.user.partner_id.is_physician:
            res['doctor_id'] = self.env.user.partner_id.id
        return res

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsultationEvaluation(models.Model):
    _name = 'consultation.evaluation'
    _description = 'Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    EVALUATION_TYPE = [
            ('Ambulatory', 'Ambulatory'),
            ('Emergency', 'Emergency'),
            ('Inpatient Admission', 'Inpatient Admission'),
            ('Pre-arraganged Appointment', 'Pre-arraganged Appointment'),
            ('Periodic Control', 'Periodic Control'),
            ('Phone Call', 'Phone Call'),
            ('Telemedicine', 'Telemedicine'),
    ]

    MOOD = [
            ('Normal', 'Normal'),
            ('Sad', 'Sad'),
            ('Fear', 'Fear'),
            ('Rage', 'Rage'),
            ('Happy', 'Happy'),
            ('Disgust', 'Disgust'),
            ('Euphoria', 'Euphoria'),
            ('Flat', 'Flat'),
    ]

    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)
    state = fields.Selection([('Clinical examination','Clinical examination'),('Additional examinations','Additional examinations'),('Diagnosis Established','Diagnosis Established')], default='Clinical examination')
    patient_id = fields.Many2one('res.partner', string='Patient', domain="[('is_patient','=',True)]", required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor',required=True)
    evaluation_start_date = fields.Datetime(string='Date d\'évaluation', required=True, default=lambda self: fields.Datetime.now())
    evaluation_end_date = fields.Datetime(string='Date de fin d\'évaluation', readonly=True)
    evaluation_type = fields.Selection(EVALUATION_TYPE, string='Type d\'évaluation', required=True, index=True, default=lambda *a: 'Pre-arraganged Appointment')




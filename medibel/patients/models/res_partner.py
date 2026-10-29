from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta 

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_patient = fields.Boolean(string="Is patient", default=False)
    confidentiality = fields.Selection([('normal','Normal'),('confidentiel','Confidentiel')], string='Confidentiality', default='normal')
    is_physician = fields.Boolean("Is a Physician", default=False)
    specialty_id = fields.Many2one("medical.specialty", string="Primary Specialty", ondelete="restrict")

    primary_physician_id = fields.Many2one("res.partner", string="Primary Care Physician",domain="[('is_physician','=',True), ('is_company','=',False)]", ondelete="restrict")
    primary_physician_specialty_id = fields.Many2one("medical.specialty",string="PCP Specialty",related="primary_physician_id.specialty_id", store=False, readonly=True,)

    # Basic Health Profile
    blood_group = fields.Selection([
        ("A", "A"), ("B", "B"), ("AB", "AB"), ("O", "O")
    ], string="Blood group")
    rh_factor = fields.Selection([("+", "Rh+"), ("-", "Rh-")], string="Rh")
    mother_id = fields.Many2one('res.partner', string="Patient's mother", domain="[('gender_id.name', '=', 'Female'),('id','!=', id)]")
    father_id = fields.Many2one('res.partner', string="Patient's father", domain="[('gender_id.name', '=', 'Male'),('id','!=', id)]")
    deceased = fields.Boolean(string='Deceased')
    date_of_death = fields.Datetime(string="Date of death")
    age_of_death = fields.Char(string='Age of death', compute="_onchange_age_of_death",store=True)
    cause_of_death = fields.Many2one('medical.pathology', string="Cause of death")  
    patient_disease_ids = fields.One2many('patient.disease','patient_id')
    extra_info = fields.Text(string="Info")
    company_id = fields.Many2one('res.company', 'Healthcare establishment')  
    user_allowed_id = fields.Many2one('res.users', string='Authorized User')


    @api.depends('date_of_birth','date_of_death')
    def _onchange_age_of_death(self):
        for rec in self:
            if rec.date_of_death:
                d1 = rec.date_of_birth
                d2 = rec.date_of_death
                rd = relativedelta(d2, d1)
                rec.age_of_death = str(rd.years) + " year(s)" +" "+ str(rd.months) + " months" +" "+ str(rd.days) + " days"
            else:
                rec.age_of_death = "No date of death!!"


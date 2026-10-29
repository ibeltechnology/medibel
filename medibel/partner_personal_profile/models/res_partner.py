from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from random import choice
from string import digits

class ResPartner(models.Model):
    _inherit = "res.partner"

    # Identity
    date_of_birth = fields.Date("Date of Birth")
    gender_id = fields.Many2one('medical.gender', string="Gender")
    marital_status = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("widowed", "Widowed"),
        ],
        string="Marital Status",
    )
    nationality_id = fields.Many2one("res.country", string="Nationality")
    # Identity document
    id_type = fields.Selection(
        [
            ("nid", "National ID"),
            ("passport", "Passport"),
            ("permit", "Driver's License"),
            ("other", "Other"),
        ],
        string="ID Type",
    )
    id_number = fields.Char("ID Number")
    id_issue_date = fields.Date("Issue Date")
    id_expiry_date = fields.Date("Expiry Date")
    # Emergency
    emergency_contact_id = fields.Many2one("res.partner", string="Emergency Contact")
    emergency_phone = fields.Char("Emergency Phone")

    # Location
    patient_country_id = fields.Many2one('res.country', 'Country of residence')   
    region_id = fields.Many2one('region.region', string='Region', domain="[('res_country_id', '=', patient_country_id)]", help='')
    departement_id = fields.Many2one('departement.departement', string='Département', domain="[('region_id', '=', region_id)]", help='')
    arrondissement_id = fields.Many2one('arrondissement.arrondissement', string='Arrondissement', domain="[('departement_id', '=', departement_id)]", help='')
    commune_id = fields.Many2one('commune.commune', string='Commune', domain="[('arrondissement_id', '=', arrondissement_id)]", help='')
    # Age & bracket (computed)
    age_years = fields.Float("Age (years)", compute="_compute_age_fields", store=False)
    age_display = fields.Char("Age (display)", compute="_compute_age_fields", store=False)
    age_days = fields.Integer(string="Age", readonly=True, compute="_compute_age_days")
    age_range_id = fields.Many2one("patient.age.range", "Tranche d'age", compute="_compute_age_range_id", store=True,)

    barcode = fields.Char(string='Barcode',readonly=True, copy=False, index=True, help='Patient barcode')

    def generate_random_barcode(self):
        for patient in self:
            patient.barcode = '041'+"".join(choice(digits) for i in range(9))

    @api.depends("date_of_birth")
    def _compute_age_fields(self):
        today = fields.Date.context_today(self)
        for partner in self:
            dob = partner.date_of_birth
            if not dob or dob > today:
                partner.age_years = 0.0
                partner.age_display = ""
                continue

            delta = relativedelta(today, dob)
            years_float = delta.years + (delta.months / 12.0) + (delta.days / 365.0)
            partner.age_years = round(years_float, 2)

            if delta.years >= 2:
                txt = f"{delta.years} years"
                if delta.months:
                    txt += f" {delta.months} mo"
            elif delta.years == 1:
                txt = "1 year"
                if delta.months:
                    txt += f" {delta.months} mo"
            else:
                if delta.months >= 1:
                    txt = f"{delta.months} mo"
                    if delta.days:
                        txt += f" {delta.days} d"
                else:
                    total_days = (today - dob).days
                    txt = f"{total_days} d"
            partner.age_display = txt


    @api.depends('date_of_birth')
    def _compute_age_days(self):
        for rec in self:
            if rec.date_of_birth:
                today = datetime.today().date()
                rec.age_days = abs((today - rec.date_of_birth).days)
            else:
                rec.age_days = 0

    @api.depends("age_days")
    def _compute_age_range_id(self):
        age_ranges = self.env["patient.age.range"].search([])
        for record in self:
            if not record.age_days:
                age_range = False
            else:
                age_range = (
                    age_ranges.filtered(
                        lambda age_range: age_range.age_from
                        <= record.age_days
                        <= age_range.age_to
                    )
                    or False
                )
            if record.age_range_id != age_range:
                record.age_range_id = age_range and age_range.id or age_range

    @api.model
    def _cron_update_age_range_id(self):
        """
        This method is called from a cron job.
        It is used to update age range on contact
        """
        partners = self.search([("date_of_birth", "!=", False)])
        partners._compute_age_range_id()
        
#    @api.model_create_multi
#    def create(self, vals_list):
#        for vals in vals_list:
#            partner_id  = self.env['ir.sequence'].next_by_code('res.partner')
#            if partner_id:
#                vals.update({
#                        'identification_code':partner_id,
#                       })
#            return super().create(vals_list)
            
#    @api.model_create_multi
#    def create(self, vals):
#        """ override the create function to apply the sequence code in our custom model records """
#        if vals.get('identification_code', 'New') == 'New':
#            vals['identification_code'] = self.env['ir.sequence'].next_by_code('res.partner') or 'New'
#        return super(ResPartner, self).create(vals)

    @api.constrains("is_patient", "gender_id")
    def _check_gender_required(self):
        for rec in self:
            if rec.is_patient and not rec.gender_id:
                raise ValidationError("The patient's gender must be entered.")
                

    _barcode_uniq = models.Constraint(
        'unique (barcode)', 
        "The Badge ID must be unique, it is already assigned to a patient."
    )
    

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PrescriptionOrder(models.Model):
    _name = 'prescription.order'
    _description = 'prescription.order'
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
    _mail_post_access = "read"
    

    name = fields.Char(string='Nom', required=True)
    active = fields.Boolean(string='Actif', default=True)
    prescription_date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    doctor_id = fields.Many2one(string='Prescribing physician', comodel_name='res.users', default=lambda self: self.env.user, readonly=True)
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner', domain="[('is_patient', '=', True)]")
    prescription_line_ids = fields.One2many(string='Prescription lines', comodel_name='prescription.line', inverse_name='prescription_id')
    notes = fields.Text(string='Notes')
    doctor_name = fields.Char(string="Prescribing physician name", compute="_compute_doctor_name", compute_sudo=True,readonly=True,)

    @api.depends("doctor_id")
    def _compute_doctor_name(self):
        for prescription in self:
            prescription.doctor_name = (
                prescription.doctor_id.name
                if prescription.doctor_id
                else False
            )
    
    def _compute_access_url(self):
        super()._compute_access_url()
        for prescription in self:
            prescription.access_url = (
                f"/my/prescriptions/{prescription.id}"
            )


    def _get_report_base_filename(self):
        self.ensure_one()
        return f"Ordonnance_{self.name or self.id}"



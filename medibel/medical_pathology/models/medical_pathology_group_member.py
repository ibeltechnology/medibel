# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MedicalPathologyGroupMember(models.Model):
    _name = 'medical.pathology.group.member'
    _description = "Medical Pathology Group Member"

    disease_group_id = fields.Many2one('medical.pathology.group', string="Group", required=True)

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Arrondissement(models.Model):
    _name="arrondissement.arrondissement"
    _description = "Arrondissement"

    name = fields.Char('Arrondissement',required=True)
    region_id = fields.Many2one('region.region', string='Région')
    departement_id = fields.Many2one('departement.departement',string="Department",)
    commune_ids = fields.One2many('commune.commune','arrondissement_id', string='communes')
    commune_ids_count = fields.Integer(compute="_compute_commune_ids")

    def _compute_commune_ids(self):
        for record in self:
            record.commune_ids_count = self.env['commune.commune'].search_count([('arrondissement_id', '=', self.id)])


    def get_region_id_commune_ids(self):
        related_communes = self.env['commune.commune'].search([('arrondissement_id', '=', self.id)])
        action = self.env.ref('senegal.action_commune').read()[0]
        if len(related_communes) > 1:
            action['domain'] = [('id', 'in', related_communes.ids)]
            action['context'] = {'default_arrondissement_id': self.id}
        elif len(related_communes) == 1:
            action['context'] = {'default_arrondissement_id': self.id}
            action['views'] = [(self.env.ref('senegal.commune_form_view').id, 'form')]
            action['res_id'] = related_communes.ids[0]
        return action
    


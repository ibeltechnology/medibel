# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Region(models.Model):
    _name="departement.departement"
    _description = "Departement"

    name = fields.Char('Departement de',required=True)
    code = fields.Char('Code')
    region_id = fields.Many2one('region.region', string="Région")
    arrondissement_ids = fields.One2many('arrondissement.arrondissement','departement_id', string='Arrondissements')
    arrondissement_ids_count = fields.Integer(compute="_compute_arrondissement_ids")
    commune_ids = fields.One2many('commune.commune','departement_id', string='communes')
    commune_ids_count = fields.Integer(compute="_compute_commune_ids")
    

    def _compute_arrondissement_ids(self):
        for record in self:
            record.arrondissement_ids_count = self.env['arrondissement.arrondissement'].search_count([('departement_id', '=', self.id)])


    def get_region_id_arrondissement_ids(self):
        related_arrondissements = self.env['arrondissement.arrondissement'].search([('departement_id', '=', self.id)])
        action = self.env.ref('senegal.action_arrondissement').read()[0]
        if len(related_arrondissements) > 1:
            action['domain'] = [('id', 'in', related_arrondissements.ids)]
            action['context'] = {'default_departement_id': self.id}
        elif len(related_arrondissements) == 1:
            action['context'] = {'default_departement_id': self.id}
            action['views'] = [(self.env.ref('senegal.arrondissement_form_view').id, 'form')]
            action['res_id'] = related_arrondissements.ids[0]
        return action
            
    def _compute_commune_ids(self):
        for record in self:
            record.commune_ids_count = self.env['commune.commune'].search_count([('departement_id', '=', self.id)])


    def get_region_id_commune_ids(self):
        related_communes = self.env['commune.commune'].search([('departement_id', '=', self.id)])
        action = self.env.ref('senegal.action_commune').read()[0]
        if len(related_communes) > 1:
            action['domain'] = [('id', 'in', related_communes.ids)]
            action['context'] = {'default_departement_id': self.id}
        elif len(related_communes) == 1:
            action['context'] = {'default_departement_id': self.id}
            action['views'] = [(self.env.ref('senegal.commune_form_view').id, 'form')]
            action['res_id'] = related_communes.ids[0]
        return action
    
    


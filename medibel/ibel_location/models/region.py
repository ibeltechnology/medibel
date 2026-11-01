# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Region(models.Model):

    _name="region.region"
    _description = "Region"

    name = fields.Char('Region de',required=True)
    code = fields.Char('Code')
    res_country_id = fields.Many2one('res.country', string="Pays")   
    departement_ids = fields.One2many('departement.departement','region_id', string='Departements')
    departement_ids_count = fields.Integer(compute="_compute_departement_ids")
    arrondissement_ids = fields.One2many('arrondissement.arrondissement','region_id', string='Arrondissements')
    arrondissement_ids_count = fields.Integer(compute="_compute_arrondissement_ids")
    commune_ids = fields.One2many('commune.commune','region_id', string='communes')
    commune_ids_count = fields.Integer(compute="_compute_commune_ids")
 
    def _compute_departement_ids(self):
        for record in self:
            record.departement_ids_count = self.env['departement.departement'].search_count([('region_id', '=', self.id)])


    def get_region_id_departement_ids(self):
        related_departements = self.env['departement.departement'].search([('region_id', '=', self.id)])
        action = self.env.ref('senegal.action_departement').read()[0]
        if len(related_departements) > 1:
            action['domain'] = [('id', 'in', related_departements.ids)]
            action['context'] = {'default_region_id': self.id}
        elif len(related_departements) == 1:
            action['context'] = {'default_region_id': self.id}
            action['views'] = [(self.env.ref('senegal.departement_form_view').id, 'form')]
            action['res_id'] = related_departements.ids[0]
        return action
 
    def _compute_arrondissement_ids(self):
        for record in self:
            record.arrondissement_ids_count = self.env['arrondissement.arrondissement'].search_count([('region_id', '=', self.id)])


    def get_region_id_arrondissement_ids(self):
        related_arrondissements = self.env['arrondissement.arrondissement'].search([('region_id', '=', self.id)])
        action = self.env.ref('senegal.action_arrondissement').read()[0]
        if len(related_arrondissements) > 1:
            action['domain'] = [('id', 'in', related_arrondissements.ids)]
            action['context'] = {'default_region_id': self.id}
        elif len(related_arrondissements) == 1:
            action['context'] = {'default_region_id': self.id}
            action['views'] = [(self.env.ref('senegal.arrondissement_form_view').id, 'form')]
            action['res_id'] = related_arrondissements.ids[0]
        return action
        
        
    def _compute_commune_ids(self):
        for record in self:
            record.commune_ids_count = self.env['commune.commune'].search_count([('region_id', '=', self.id)])


    def get_region_id_commune_ids(self):
        related_communes = self.env['commune.commune'].search([('region_id', '=', self.id)])
        action = self.env.ref('senegal.action_commune').read()[0]
        if len(related_communes) > 1:
            action['domain'] = [('id', 'in', related_communes.ids)]
            action['context'] = {'default_region_id': self.id}
        elif len(related_communes) == 1:
            action['context'] = {'default_region_id': self.id}
            action['views'] = [(self.env.ref('senegal.commune_form_view').id, 'form')]
            action['res_id'] = related_communes.ids[0]
        return action

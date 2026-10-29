# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MedicalPathologyCategory(models.Model):
    _name = 'medical.pathology.category'
    _description = "Medical Pathology Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'
    
    name = fields.Char(string="Category Name",required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True ,recursive=True,)
    active = fields.Boolean(string="Active" , default = True)
    parent_id = fields.Many2one('medical.pathology.category', string="Parent Category", index=True, ondelete='cascade')
    parent_path = fields.Char(index=True,)
    child_ids = fields.One2many('medical.pathology.category', 'parent_id', 'Child Categories')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
                
    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if  self._has_cycle():
            raise ValidationError(_('You cannot create recursive categories.'))
        return True

    pathology_ids = fields.One2many('medical.pathology', 'category_id', string='Maladies')
    pathology_ids_count = fields.Integer(compute="_compute_pathology_ids")
 
    def _compute_pathology_ids(self):
        for record in self:
            record.pathology_ids_count = self.env['medical.pathology'].search_count([('category_id', '=', self.id)])
            
    def action_pathology(self):
        self.ensure_one()
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'medical.pathology',
            'name': 'Maladies',
            'domain':[('category_id', '=', self.id)],
#            'context': {'search_default_category_id': self.id, 'default_category_id': self.id}
        }
        return view


# -*- coding:utf-8 -*-
from odoo import models, fields, api, exceptions, _

class PatientRange(models.Model):
    _name = "patient.age.range"
    _description = "patient.age.range"

    def _default_age_from(self):
        age_from = 0
        last_age_range = self.env["patient.age.range"].search(
            [], order="age_to desc", limit=1
        )
        if last_age_range:
            age_from = last_age_range.age_to + 1
        return age_from

    name = fields.Char(string="Name", required=True)
    age_from = fields.Integer(string="De", required=True, default=lambda self: self._default_age_from())
    age_to = fields.Integer(string="à", required=True)
    active = fields.Boolean('Active', default=True)

    _name_uniq = models.Constraint(
        'unique (name)', 
        "A name must be unique !"
    )

    @api.constrains("age_from", "age_to")
    def _validate_range(self):
        for rec in self:
            if rec.age_from >= rec.age_to:
                raise exceptions.ValidationError(
                    _("%s is not a valid range (%s >= %s)")
                    % (rec.name, rec.age_from, rec.age_to)
                )
            range_id = rec.search(
                [
                    ("age_from", "<=", rec.age_to),
                    ("age_to", ">=", rec.age_from),
                    ("id", "!=", rec.id),
                ],
                limit=1,
            )
            if range_id:
                raise exceptions.ValidationError(
                    _("%s is overalapping with range %s") % (rec.name, range_id.name)
                )



from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence asc, name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(default=1)

    _sql_constraints = [
        (
            "type_name_unique",
            "UNIQUE (name)",
            "Impossible to set this name : another property type with the same name already exists."
        )
    ]
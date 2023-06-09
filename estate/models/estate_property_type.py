from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "type_name_unique",
            "UNIQUE (name)",
            "Impossible to set this name : another property type with the same name already exists."
        )
    ]
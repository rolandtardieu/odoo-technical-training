from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "tag_name_unique",
            "UNIQUE (name)",
            "Impossible to set this name : another tag with the same name already exists."
        )
    ]

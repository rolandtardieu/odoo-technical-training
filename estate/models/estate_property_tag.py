from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            "tag_name_unique",
            "UNIQUE (name)",
            "Impossible to set this name : another tag with the same name already exists."
        )
    ]

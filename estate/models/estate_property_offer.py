from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for prop in self:
            if prop.create_date is not None:
                start_date = prop.create_date
            else:
                start_date = fields.Date.today()
            prop.date_deadline = start_date + relativedelta(days=prop.validity)

    def _inverse_date_deadline(self):
        for prop in self:
            if prop.create_date is not None:
                start_date = prop.create_date
            else:
                start_date = fields.Date.today()
            prop.validity = relativedelta(start_date, prop.date_deadline).days
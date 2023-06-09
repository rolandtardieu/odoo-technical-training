from datetime import datetime, timedelta

from odoo import models, fields, api, exceptions


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

    _sql_constraints = [
        ("offer_price_spositive", "CHECK (price > 0)", "An offer price has to be strictly positive.")
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date is not None:
                start_date = offer.create_date
            else:
                start_date = datetime.today()
            offer.date_deadline = start_date.date() + timedelta(offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date is not None:
                start_date = offer.create_date
            else:
                start_date = datetime.today()
            offer.validity = (offer.date_deadline - start_date.date()).days

    def action_accept(self):
        for offer in self:
            if offer.status == "refused":
                raise exceptions.UserError("Impossible to accept this offer : it has already been refused.")
            prop = self.property_id
            if prop.state == "offer_accepted" or prop.state == "sold":
                raise exceptions.UserError("Impossible to accept this offer : an offer have already been accepted.")
            if prop.state == "canceled":
                raise exceptions.UserError("Impossible to accept this offer : the sale have been canceled.")

            offer.status = "accepted"
            prop.state = "offer_accepted"
            prop.selling_price = offer.price
            prop.buyer_id = offer.partner_id

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                raise exceptions.UserError("Impossible to refuse this offer : it has been accepted yet.")
            offer.status = "refused"

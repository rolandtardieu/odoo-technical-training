from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta

from odoo.tools import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ("expected_price_spositive", "CHECK (expected_price > 0)", "The expected price has to be strictly positive."),
        ("selling_price_positive", "CHECK (selling_price >= 0)", "The selling price has to be positive.")
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for prop in self:
            if prop.state == "offer_accepted" or prop.state == "sold":
                if float_compare(prop.selling_price, 0.9 * prop.expected_price) < 0:
                    raise exceptions.ValidationError("The selling price cannot be less than 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            max_price = 0
            for offer in prop.offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            prop.best_price = max_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise exceptions.UserError("Impossible to sell a canceled property.")
        return True

    def action_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise exceptions.UserError("Impossible to cancel a sold property.")
        return True



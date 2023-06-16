from odoo import models, Command


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("Méthode action_sold overridée par le module estate_account.")

        self.env['account.move'].create({
            'partner_id': super().buyer_id._origin.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': 'Commission : 6.00% of the selling price',
                    'quantity': 1,
                    'price_unit': super().selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 10000
                }),
            ]
        })
        return super().action_sold()

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseReport(models.TransientModel):
    _name = 'purchase.wizard'

    def _get_default_purchase(self):
        return self.env["yc.purchase"].browse(self.env.context.get('active_ids'))

    purchase_ids = fields.Many2many("yc.purchase",string="purchase search", default="_get_default_purchase")
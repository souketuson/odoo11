# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseReport(models.TransientModel):
    _name = 'purchase.report'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        pass
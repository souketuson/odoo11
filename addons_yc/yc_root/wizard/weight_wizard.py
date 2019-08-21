# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YcWeightWizard(models.TransientModel):
    _name = 'yc.weight.wizard'

    start_date = fields.Date()
    end_date = fields.Date()
    driver_id = fields.Many2one('yc.driver')
    weight_ids = fields.Many2many('yc.weight')

    def search_driver(self):
        weight = self.env['yc.weight']
        domain = ()
        if self.start_date and self.end_date:
            domain += ('day', '>=', self.start_date),
            domain += ('day', '<=', self.end_date),
        if self.driver_id:
            domain += ('driver_id', '=', self.driver_id)
        if len(domain) > 0:
            records = weight.search([d for d in domain])
            self.weight_ids = [(4, record.id) for record in records]

        return {"type": "set_scrollTop"}
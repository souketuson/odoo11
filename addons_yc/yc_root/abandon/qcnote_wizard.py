# -*- coding: utf-8 -*-
from odoo import models, fields, api

class YcQcnteWizard(models.TransientModel):
    _name = "yc.qcnote.wizard"
    name = fields.Char("搜尋內容")
    qcnote_ids = fields.Many2many("yc.setqcnote", string="品管備註")

    @api.onchange('name')
    def _search(self):
        if self.name:
            self.qcnote_ids = [(5, 0, 0)]
            records = self.env['yc.setqcnote'].search([('name', 'like', self.name)])
            self.qcnote_ids = [(4, record.id) for record in records]
        else:
            self.qcnote_ids = self.env["yc.setqcnote"].search([])
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YcShipmentWizard(models.TransientModel):
    _name = 'yc.shipment.wizard'

    infurn = fields.Boolean("包含已進爐", default=False)
    verified = fields.Boolean("包含已檢驗", default=False)
    weighted = fields.Boolean("包含已過磅", default=False)
    noshiped = fields.Boolean("不含已出貨", default=False)

    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")

    @api.onchange("infurn", "verified", "weighted", "noshiped")
    def _filter_order(self):
        infurn_code = self.env['yc.setstatus'].search([('name', '=', '己進爐')]).id
        domain = ()
        if self.infurn:
            domain += ('status', '=', infurn_code),
        if self.verified:
            domain += ('checkstate', '!=', None),
        if self.weighted:
            domain += ('weighstate', '=', '已過磅'),
        # if self.noshiped:
        #     domain += (),
        if len(domain) > 0:
            purchase = self.env["yc.purchase"]
            records = purchase.search([(d) for d in domain])
            for rec in self:
                rec.purchase_ids = [(4, record.id) for record in records]

    @api.multi
    def comfirm(self):
        wizard_checked = self.purchase_ids.search([('wizard_check', '=', True)])
        # 目前進貨單current record : self._context.get('active_ids')
        source_list = self.env['yc.shipment'].browse(self._context.get('active_ids'))
        for wizard in wizard_checked:
            source_list.ship_details_ids = [(0, 0, {'order': wizard.name})]
            wizard_checked.wizard_check = False

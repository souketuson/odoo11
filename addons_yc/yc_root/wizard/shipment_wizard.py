# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YcShipmentWizard(models.TransientModel):
    _name = 'yc.shipment.wizard'

    infurn = fields.Boolean("包含已進爐", default=True)
    verified = fields.Boolean("包含已檢驗", default=True)
    weighted = fields.Boolean("包含已過磅", default=True)
    noshiped = fields.Boolean("不含已出貨", default=True)

    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")

    @api.onchange("infurn", "verified", "weighted", "noshiped")
    def _filter_order(self):
        ship = self.env['yc.shipment']
        customer = ship.browse(self._context['active_id']).customer_id
        infurn_code = self.env['yc.setstatus'].search([('name', '=', '己進爐')]).id
        domain = ()
        domain += ('checkstate', 'in', ['檢驗合格', '檢驗不合格']),
        domain += ('customer_id', '=', customer.id),
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
            records = purchase.search([(d) for d in domain], limit=100, order='id DESC')
            self.purchase_ids = [(6, 0, records.ids)]

    @api.multi
    def comfirm(self):
        wizard_checked = self.purchase_ids.search([('wizard_check', '=', True)])
        # 目前進貨單current record : self._context.get('active_ids')
        record = self.env['yc.shipment'].browse(self._context.get('active_ids'))
        for ref in wizard_checked:
            # 從進貨單拉資料進來
            record.ship_details_ids = [
                (0, 0, {'order': ref.name, 'furnace': ref.order_furn, 'product_code': ref.product_code,
                        'norm_code': ref.norm_code, 'txtur_code': ref.txtur_code, 'buckets': ref.weighbuckets,
                        'unit': ref.unit1, 'tweight': ref.tweight, 'elecpl_code': ref.elecpl_code,
                        'process1': ref.process1, 'batch': ref.batch, 'fulorhaf': ref.fulorhaf,
                        # 'fullorhalf': ref.fullorhalf,
                        'process2': ref.process2, 'day': ref.day, 'wire_furn': ref.wire_furn,
                        'proces_code': ref.proces_code, }
                 )]
            # 解掉被標註checked的工令
            ref.wizard_check = False

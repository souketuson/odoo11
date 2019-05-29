# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseWizard(models.TransientModel):
    _name = 'purchase.wizard'

    product_code = fields.Many2one("yc.setproduct", string="品名")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    productname = fields.Many2one("yc.setproduct", string="產品名稱")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    len_code = fields.Many2one("yc.setlength", string="長度")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    wire_furn = fields.Char("線材爐號")
    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")

    # 過濾查詢條件
    @api.onchange('product_code','clsf_code','productname','norm_code','proces_code','len_code','txtur_code'
                  ,'strength_level','wire_furn')
    def search_purchase(self):
        domain = ()
        if self.product_code.id:
            domain = ('product_code', '=', self.product_code.id),
        if self.clsf_code.id:
            domain += ('clsf_code', '=', self.clsf_code.id),
        if self.productname.id:
            domain += ('productname', '=', self.productname.id),
        if self.norm_code.id:
            domain += ('norm_code', '=', self.norm_code.id),
        if self.proces_code.id:
            domain += ('proces_code', '=', self.proces_code.id),
        if self.len_code.id:
            domain += ('len_code', '=', self.len_code.id),
        if self.txtur_code.id:
            domain += ('txtur_code', '=', self.txtur_code.id),
        if self.strength_level.id:
            domain += ('strength_level', '=', self.strength_level.id),
        if self.wire_furn:
            domain += ('wire_furn', '=', self.wire_furn),
        if len(domain)>0:
            purchase = self.env['yc.purchase']
            records = purchase.search([(d) for d in domain])
            for rec in self:
                # 搜尋並列表
                rec.purchase_ids = [(4, record.id) for record in records]

    # 把表面硬度,心部硬度,試片,抗拉強度,滲碳層,以前爐號,扭力,回火溫度,預排爐號 帶入到現在的進貨單
    @api.multi
    def comfirm(self):
        wizard_checked = self.purchase_ids.search([('wizard_check','=',True)])
        if len(wizard_checked)>1:
            for to_uncheck in wizard_checked:
                to_uncheck.wizard_check = False
        if len(wizard_checked) ==1:
            # 解掉checked
            wizard_checked.wizard_check = False
            # 目前進貨單current record : self._context.get('active_ids')
            for source_list in self.env['yc.purchase'].browse(self._context.get('active_ids')):
                source_list.surfhrd = wizard_checked.surfhrd
                source_list.corehrd = wizard_checked.corehrd
                source_list.piece = wizard_checked.piece
                source_list.tensihrd = wizard_checked.tensihrd
                source_list.carburlayer = wizard_checked.carburlayer
                source_list.torsion = wizard_checked.torsion
                source_list.retempt = wizard_checked.retempt
                source_list.order_furn = wizard_checked.order_furn

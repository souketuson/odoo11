# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseWizard(models.TransientModel):
    _name = 'purchase.wizard'

    def _search_purchase(self):
        domain = ('product_code','=', self.proces_code),('clsf_code','=',self.clsf_code),('productname','=',self.productname),\
                 ('norm_code','=',self.norm_code),('proces_code','=',self.proces_code),('len_code','=',self.len_code),('txtur_code','=',self.txtur_code),\
                 ('strength_level','=',self.strength_level),('wire_furn','=',self.wire_furn)
        return self.env["yc.purchase"].search([domain])

    product_code = fields.Many2one("yc.setproduct", string="品名")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    productname = fields.Many2one("yc.setproduct", string="產品名稱")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    len_code = fields.Many2one("yc.setlength", string="長度")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    wire_furn = fields.Char("線材爐號")

    purchase_ids = fields.Many2many("yc.purchase",string="purchase search")
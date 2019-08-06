from odoo import models, fields, api
from datetime import datetime as dt


class YcReturn(models.Model):
    _name = "yc.return"
    name = fields.Char("出貨退回編號")
    order = fields.Char("退回工令號碼")
    neworder = fields.Char("新工令號碼")
    day = fields.Date("退回日期", default=fields.Date.today)
    ardebitday = fields.Date("應收帳款扣款日期", default=fields.Date.today)
    followup = fields.Selection([("migrate", "轉入進貨單"), ("stay", "不轉入進貨單")], "處理方式")
    byear = fields.Char("所屬帳款年")
    bmonth = fields.Char("所屬帳款月")
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    pc = fields.Many2one("res.users", string="生管人員", default=lambda self: self.env.user)
    customer_code = fields.Char()
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    note = fields.Char("退回備註")
    bukets = fields.Integer("退回桶數")
    weight = fields.Integer("退回重量")
    money = fields.Integer("退回金額")
    factory_id = fields.Many2one("yc.factory", string="所屬工廠", default=lambda self: self.env.user.factory_id)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.user.company_id)
    wizard_check = fields.Boolean("是否帶出", default=False, help='checkbox TorF判斷要帶出哪筆資料')
    # 一個退回 對應 一個工令
    # 一個工令 對應 一個退回

    purchase_id = fields.Many2one('yc.purchase')
    product_id = fields.Char(related='purchase_id.product_code.name')
    order_id = fields.Char(related='purchase_id.name')
    norm_code = fields.Char(related='purchase_id.norm_code.name')
    currnt_furno = fields.Char(related="purchase_id.currnt_furno.name")
    txtur_code = fields.Char(related="purchase_id.txtur_code.name")
    weighbuckets = fields.Integer(related="purchase_id.weighbuckets")
    unit1 = fields.Char(related="purchase_id.unit1.name")
    tweight = fields.Integer(related="purchase_id.tweight")
    elecpl_code = fields.Char(related="purchase_id.elecpl_code.name")
    fullorhalf = fields.Selection(related="purchase_id.fullorhalf")
    purchase_day = fields.Date(related="purchase_id.day")
    wire_furn = fields.Char(related="purchase_id.wire_furn")
    proces_code = fields.Char(related="purchase_id.proces_code.name")

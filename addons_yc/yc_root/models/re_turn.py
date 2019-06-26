from odoo import models, fields, api
from datetime import datetime as dt


class YcReturn(models.Model):
    _name = "yc.return"
    name = fields.Char("出貨退回編號")
    order = fields.Char("退回工令號碼")
    neworder = fields.Char("新工令號碼")
    day = fields.Date("進貨日期", default=dt.today())
    ardebitday = fields.Datetime("應收帳款扣款日期")
    followup = fields.Char("處理方式")
    byear = fields.Char("所屬帳款年")
    bmonth = fields.Char("所屬帳款月")
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    pc = fields.Many2one("res.users", string="生管人員", default=lambda self: self.env.user)
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    note = fields.Char("退回備註")
    bukets = fields.Integer("退回桶數")
    weight = fields.Integer("退回重量")
    money = fields.Integer("退回金額")
    factory_id = fields.Many2one("yc.factory", string="所屬工廠", default=lambda self: self.env.user.factory_id)

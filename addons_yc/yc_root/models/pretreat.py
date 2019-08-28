# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime as dt


class YcPretreat(models.Model):
    _name = "yc.pretreat"

    day = fields.Date()
    name = fields.Char()
    customer_id = fields.Many2one('yc.customer')
    processing_id = fields.Many2one("yc.processing", "加工廠名稱")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    nums = fields.Integer()
    unit = fields.Many2one('yc.setunit')
    ck = fields.Boolean()

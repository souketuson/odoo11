# -*- coding: utf-8 -*-


from odoo import models, fields, api


class YcFake(models.Model):
    _name = "yc.fake"
    name = fields.Char("___")

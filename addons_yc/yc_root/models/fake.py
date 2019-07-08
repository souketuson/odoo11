# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime as dt
import re


class YcFake(models.Model):
    _name = "yc.fake"
    _description = 'Book'
    name=fields.Char('name')

    tem = fields.Date()
    diplay = fields.Date()

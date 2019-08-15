# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime as dt
import re, tempfile, base64,binascii
from xlrd import open_workbook
from odoo.tools.mimetypes import guess_mimetype

class YcFake(models.Model):
    _name = "yc.fake"
    _description = 'Book'
    name=fields.Char('name')

    tem = fields.Date()
    diplay = fields.Date()
    file = fields.Binary("檔案")
    data_get = fields.Char()

    @api.onchange('data_get')
    def _get_data(self):
        data = open_workbook("C:/Users/User/Desktop/新增資料夾/1.xlsx")
        table = data.sheets()[0]



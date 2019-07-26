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
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        workbook = open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)


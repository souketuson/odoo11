# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt


class YcWeight(models.Model):
    _name = "yc.weight"

    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    name = fields.Char("過磅單號", default=lambda self: self.env["ir.sequence"].next_by_code("WeightList.sequence"))

    # 要改成自動編號 & 上鎖
    @api.multi
    @api.onchange("name")
    def _generate(self):
        '''WL + 190227 + 001...999
                    2    +  6          + 3

                    '''
        # prefix WL + yymmdd
        _serial = 'WL' + dt.today().strftime("%y%m%d")
        # search today's last one data on db
        _next = 0
        obj = self.env['yc.weight'].search([('name', '=like', _serial + "%")], limit=1, order='name DESC')
        if obj:  # 如果無/有系列碼
            _next = int(obj[0].name[8:]) + 1
            _serial += '%03d' % _next
        else:
            _serial += '001'
        self.name = _serial

    day = fields.Date("過磅日期", default=dt.today())

    weightime = fields.Datetime("過磅時間", default=lambda self: dt.strptime(dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                         "%Y-%m-%d %H:%M:%S"))
    person_id = fields.Many2one("yc.hr", string="過磅員")
    weighbridge = fields.Char("地磅序號")
    carno = fields.Char("車次序號")

    # carno = S1+S2+S3+S4+S5
    def _generate_carno(self):
        if dt.now().strftime("%Y-%m-%d"):
            pass

    in_out = fields.Selection([('I', '進貨'), ('O', '出貨')], '進出貨')
    factory_id = fields.Many2one("yc.factory", string="所屬工廠")

    purchase_times = fields.Integer("進貨次數", compute="_count", store=True)
    ship_times = fields.Integer("出貨次數", compute="_count", store=True)

    # 進出貨次數自動記錄
    @api.multi
    @api.depends('in_out')
    def _count(self):
        for rec in self: 
            check_day = dt.strptime(rec.day, "%Y-%m-%d")
            pn = rec.plate_no
            check_in = rec.env["yc.weight"].search(
                [('in_out', '=', 'I'), ('day', '=', check_day), ('plate_no', '=', pn)])
            check_out = rec.env["yc.weight"].search(
                [('in_out', '=', 'O'), ('day', '=', check_day), ('plate_no', '=', pn)])
            if rec.in_out:  # 進出貨有值
                if pn and rec.day:  # 車牌&日期 有值
                    if rec.in_out == 'I':
                        self.ship_times = len(check_out)
                        self.purchase_times = len(check_in) + 1
                    elif rec.in_out == 'O':
                        self.ship_times = len(check_out) + 1
                        self.purchase_times = len(check_in)
                else:  # 進出貨 空值
                    pass
            else:
                pass

    @api.constrains("in_out")
    def _verify(self):
        if not self.in_out:
            raise Warning("進出貨分類空值")

    plate_no = fields.Char("車號", compute="_auto_fetch_plateno", store=True)

    # 選完司機名稱 車牌自動帶入
    @api.depends("driver_id")
    def _auto_fetch_plateno(self):
        for rec in self:
            if rec.driver_id:
                rec.plate_no = self.env["yc.driver"].search([('name', '=', self.driver_id.name)]).plate_no
            else:
                pass

    total = fields.Integer("總重 (KG)")
    curbweight = fields.Integer("空車重 (KG)")
    other = fields.Integer("其他重量 (KG)")
    emptybucket = fields.Integer("空桶重 (KG)")
    net = fields.Integer("淨重 (KG)", compute="_NetWeight")
    note = fields.Char("備註")

    # 改成自動計算

    def _NetWeight(self):
        self.net = self.total - self.curbweight - self.emptybucket

    refine = fields.Integer("調質重量 (KG)")
    carbur = fields.Float("滲碳單價")
    other1 = fields.Integer("其他重量1")

    # 一張過磅單 上面的貨物可能含有多家客戶
    customer_detail_ids = fields.One2many("yc.weight.details", "name", "客戶明細")


class YcWeightDetails(models.Model):
    _name = "yc.weight.details"

    name = fields.Many2one("yc.weight", "訂單編號", ondelete="cascade")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    processing_id = fields.Many2one("yc.processing", "加工廠名稱")
    note = fields.Char("備註")


class YcPurchase(models.Model):
    _name = "yc.purchase"

    name = fields.Char("進貨單號")

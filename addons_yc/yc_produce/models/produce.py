# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt
from time import gmtime, strftime


class YcWeight(models.Model):
    _name = "yc.weight"

    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    name = fields.Char("過磅單號", default=lambda self: self.env["ir.sequence"].next_by_code("WeightList.sequence"))

    # 要改成自動編號 & 上鎖
    @api.model
    def _generate(self):
        '''WL + 190227 + 001...999
                    2    +  6          + 3
                    '''
        # prefix WL + yy-mm-dd
        _serial = 'WL' + dt.today().strftime("%y%m%d")
        # search db of today's last one data
        obj = self.env['yc.weight'].search([('name', '=like', _serial + "%")], limit=1, order='name DESC')
        if obj:  # 如果有系列碼
            _next = int(obj[0].name[8:]) + 1
            _serial += '%03d' % _next
        elif not obj:
            _serial += '001'

        self.name = _serial

    day = fields.Date("過磅日期", default=dt.today())

    weightime = fields.Datetime("過磅時間", default=lambda self: dt.strptime(strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                                                                         "%Y-%m-%d %H:%M:%S"))
    person_id = fields.Many2one("yc.hr", string="過磅員")
    car_no = fields.Char("車次序號", default=lambda self: self.env["ir.sequence"].next_by_code("ordinal.code"))
    in_out = fields.Selection([('i', '進貨'), ('o', '出貨')], '進出貨')
    factory = fields.Many2one("yc.factory", string="所屬工廠")

    purchase_times = fields.Integer("進貨次數", compute="_count", store=True)
    ship_times = fields.Integer("出貨次數", compute="_count", store=True)

    # 進出貨次數要改成自動記錄
    @api.depends('in_out')
    def _count(self):
        for rec in self:
            check_day = dt.strptime(rec.day, "%Y-%m-%d")
            pn = rec.plate_no
            check_in = rec.env["yc.weight"].search(
                [('in_out', '=', 'i'), ('day', '=', check_day), ('plate_no', '=', pn)])
            check_out = rec.env["yc.weight"].search(
                [('in_out', '=', 'o'), ('day', '=', check_day), ('plate_no', '=', pn)])
            if rec.in_out:  # 進出貨有值
                if pn and rec.day:  # 車牌&日期 有值
                    rec.purchase_times = len(check_in)
                    rec.ship_times = len(check_out)
                else:  # 進出貨 空值
                    pass
            else:
                pass

    @api.constrains("in_out")
    def _verify(self):
        if not self.in_out:
            raise Warning("進出貨分類空值")

    plate_no = fields.Char("車號", required=True)
    total_weight = fields.Integer("總重 (KG)")
    curb_weight = fields.Integer("空車重 (KG)")
    ept_buc_weight = fields.Integer("空桶重 (KG)")
    net_weight = fields.Integer("淨重 (KG)", compute="_NetWeight")

    # 改成自動計算

    def _NetWeight(self):
        self.net_weight = self.total_weight - self.curb_weight - self.ept_buc_weight

    refine_weight = fields.Integer("調質重量 (KG)")
    carburize_weight = fields.Float("滲碳單價")
    other1 = fields.Char("其他1")
    other2 = fields.Char("其他2")

    # 一張過磅單 上面的貨物可能含有多家客戶
    customer_detail_ids = fields.One2many("yc.weight.details", "name", "客戶明細")
    # def form_time(self):
    # 檢查欄位的形式是否符合 XX:XX


class YcWeightDetails(models.Model):
    _name = "yc.weight.details"

    name = fields.Many2one("yc.weight", "訂單編號", ondelete="cascade")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    processing_id = fields.Many2one("yc.processing", "加工廠名稱")
    note = fields.Char("備註")


class YcPurchase(models.Model):
    _name = "yc.purchase"

    name = fields.Char("進貨單號")

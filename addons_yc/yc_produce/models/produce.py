# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt


class YcWeight(models.Model):
    _name = "yc.weight"

    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    name = fields.Char("過磅單號")

    # 要改成自動編號
    @api.model
    def _generate(self):
        """
        SN190227
        :return:
        """
        _prefix = 'SN' + dt.today().strftime("%y%m%d")
        # obj = self.env['yc.weight'].search([('name', '=like', _prefix + "%")], limit=1, order='name DESC')
        _prefix += '001'

        self.name = _prefix

    day = fields.Date("過磅日期", default=dt.today())
    weightime = fields.Char("過磅時間")
    person_id = fields.Many2one("yc.hr", string="過磅員")
    car_no = fields.Char("車次序號")
    in_out = fields.Selection([('i', '進貨'), ('o', '出貨')], '進出貨')
    factory = fields.Many2one("yc.factory", string="所屬工廠")

    purchase_times = fields.Integer("進貨次數", compute="_count", store=True)
    ship_times = fields.Integer("出貨次數", compute="_count", store=True)

    # 進出貨次數要改成自動記錄
    @api.depends('in_out')
    def _count(self):
        """條件
        如 車號 日期 類型 為空 pass
        同車號&同天&同類型 以及 進貨 進貨次數+1
        同車號&同天&同類型 以及 出貨 出貨次數+1
          """
        for rec in self:
            check_day = dt.strptime(rec.day, "%Y-%m-%d")
            pn = rec.plate_no
            d = rec.day
            i = rec.env["yc.weight"].search([('in_out', '=', 'i'), ('day', '=', check_day), ('plate_no', '=', pn)])
            o = rec.env["yc.weight"].search([('in_out', '=', 'o'), ('day', '=', check_day), ('plate_no', '=', pn)])
            if rec.in_out:
                if pn and d:
                    rec.purchase_times = len(i)
                    rec.ship_times = len(o)
                else:
                    if rec.in_out == 'i':
                        rec.purchase_times = 0
                    elif rec.in_out == 'o':
                        rec.ship_times = 0
                    else:
                        rec.ship_times = 0
                        rec.purchase_times = 0

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

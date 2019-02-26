# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime


class YcWeight(models.Model):
    _name = "yc.weight"

    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    name = fields.Char("過磅單號")
    # 要改成自動編號
    date = fields.Date("過磅日期") 
    weightime = fields.Char("過磅時間")
    person_id = fields.Many2one("yc.hr", string="過磅員")
    car_no = fields.Char("車次序號")
    in_out = fields.Selection([('i', '進貨'), ('o', '出貨')], '進出貨')
    factory = fields.Many2one("yc.factory", string="所屬工廠")

    purchase_times = fields.Integer("進貨次數", compute="_count")
    ship_times = fields.Integer("出貨次數", compute="_count")

    # 進出貨次數要改成自動記錄

    @api.multi
    @api.onchange("weight_ids")
    def _count(self):
        """條件
        如 車號 日期 類型 為空 pass
        同車號&同天&同類型 以及 分類1 進貨次數+1
        同車號&同天&同類型 以及 分類2 出貨次數+1
          """
     #   tday = datetime.strptime(self.date, "%Y-%m-%d")
     #   self.purchase_times = len(self.env["yc.weight"].search(['date', '=', tday]))

        # self.ship_times = len(self.env["yc.weight"].search(['date', '=', tday]))

    weight_ids = fields.One2many("yc.weight", "plate_no")

    plate_no = fields.Char("車號")
    total_weight = fields.Char("總重 (KG)")
    curb_weight = fields.Char("空車重 (KG)")
    ept_buc_weight = fields.Char("空桶重 (KG)")
    net_weight = fields.Char("淨重 (KG)")

    # 改成自動計算
    def _netweight(self):
        if self.total_weight or self.curb_weight or self.ept_buc_weight == 0:
            pass
        else:
            self.net_weight = self.total_weight - self.curb_weight - self.ept_buc_weight

    refine_weight = fields.Char("調質重量 (KG)")
    carburize_weight = fields.Char("滲碳單價")
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

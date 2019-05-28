from odoo import models, fields, api
from datetime import datetime as dt


class YcShipment(models.Model):
    _name = "yc.shipment"
    name = fields.Char("貨單序號")
    day = fields.Date("出貨日期")
    acyear = fields.Char("所屬帳款年")
    acmonth = fields.Char("所屬帳款月")
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    pc = fields.Many2one("yc.hr", string="生管人員")
    voucher = fields.Char("傳票編號")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    phone = fields.Char("電話")
    fax = fields.Char("傳真")
    note = fields.Text("注意事項")
    othercost = fields.Integer("其他費用金額")
    invalornot = fields.Boolean("是否已作廢")
    description = fields.Text("明細說明")
    tbuckets = fields.Integer("總桶數")
    tweights = fields.Float("總重量")
    tmoney = fields.Float("總金額")
    factory_id = fields.Many2one("yc.factory", string="所屬工廠")

    searchorder = fields.Char("工令")
    searchfurn = fields.Char("爐號")
    searchbuk = fields.Char("桶數")
    searchunit = fields.Many2one("yc.setunit", string="單位")
    searchweight = fields.Char("桶數")
    searchfactory2 = fields.Many2one("yc.processing", string="次加工廠")
    searchcustomer2 = fields.Many2one("yc.customer", "二次廠商")
    searchnote = fields.Text("備註")



    # 到底是一張出貨單號對 多張工令
    # 還是　多張出貨單號對 多張工令
    ship_details_ids = fields.Many2many("yc.shipment.details", string="出貨明細檔")

    infurn = fields.Boolean("包含已進爐", default=False)
    verified = fields.Boolean("包含已檢驗", default=False)
    weighted = fields.Boolean("包含已過磅", default=False)
    noshiped = fields.Boolean("不含已出貨", default=False)

    @api.onchange("searchorder")
    def search_order(self):
        if self.searchorder:
            purchase = self.env["yc.purchase"]
            order = purchase.search([("name", "=", self.searchorder)])
            # ship = self.env["yc.shipment"]
            # empty_name_record = ship.search([('name', '=', None)])
            # if len(empty_name_record)>=1:
            #     sql = "delete from yc_shipment where name is NULL"
            #     self._cr.execute(sql)

            # furnace爐號所用的欄位 是yc.purchase的order_furn 還是 current_furn?
            order_dict = {'order': order.name, 'furnace': order.order_furn.id, "product_code": order.product_code.id,
                          'norm_code': order.norm_code.id,
                          'txtur_code': order.txtur_code.id,
                          'buckets': order.weighbuckets,'unit':order.unit1.id,'tweight':order.tweight,
                          'elecpl_code': order.elecpl_code.id,
                          'process1': order.process1.id, 'batch': order.batch, 'fullorhalf': order.fullorhalf,
                          'process2': order.process2.id, 'day': order.day, 'wire_furn': order.wire_furn,
                          'proces_code': order.proces_code.id,
                          }
            # 列表待出貨工令
            for rec in self:
                rec.ship_details_ids = [(0, 0, order_dict)]

    # '依日期變換 貨單序號
    #     Private Sub 出貨日期_ValueChanged(sender As System.Object, e As System.EventArgs) Handles 出貨日期.ValueChanged
    #         If MyTableStatus = 1 Then
    #             strPage = FIRMCODE + Mid(CStr(出貨日期.Value.Year - 1911), 2, 2) + 出貨日期.Value.Month.ToString.PadLeft(2, "0")
    #             '貨單序號.Text = ERP_AutoNo_貨單序號(DNS, strPage, "出貨單主檔", "貨單序號")
    # name = 登入廠 + 民國年尾2位數 + 月份(0x) + 四位數流水號

    @api.model
    def create(self, vals):
        day = vals['day']
        firm = vals['factory_id']
        fire_code = 0
        if firm==12:
            fire_code = 2
        year = int(day[0:4]) - 1911
        month = int(day[5:7])
        ship = self.env["yc.shipment"]
        prefix = str(fire_code) + str(year) + "%02d" % month
        bunch = ship.search([("name","ilike", prefix)])
        serial = len(bunch) + 1
        name = prefix + '%04d' % serial
        vals.update({'name': name})
        return super(YcShipment,self).create(vals)

    # 轉待出貨或刪除按鈕
    def toship_or_delete(self):
        # shipment = self.env['yc.shipment.details']
        # check = shipment.search([("ship_check", "=", True)])
        for i in self.ship_details_ids:
            i.ship_check


class YcShipmentDetails(models.Model):
    _name = "yc.shipment.details"
    name = fields.Char("貨單序號")

    order = fields.Char("工令號碼")
    serial = fields.Char("序號")
    buckets = fields.Integer("磅後桶數")
    unit = fields.Many2one("yc.setunit", string="單位")
    weight = fields.Float("重量")
    process1 = fields.Many2one("yc.processing", string="加工廠代號")
    furnace = fields.Many2one("yc.setfurnace", string="爐號")
    note = fields.Text("備註")
    unitprice = fields.Float("單價")
    subtotal = fields.Float("小計")
    process2 = fields.Many2one("yc.processing", string="二次加工廠代號")
    sort = fields.Integer("排序")
    batch = fields.Char("客戶批號")

    toship_check = fields.Boolean("待", default=False, help="轉待出貨")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    tweight = fields.Integer("磅後總重")
    elecpl_code = fields.Many2one("yc.setelectroplating", string="電鍍別")
    fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')
    day = fields.Date("進貨日期")
    wire_furn = fields.Char("線材爐號")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")

    ship_check = fields.Boolean("選", default=False, help="轉出貨")
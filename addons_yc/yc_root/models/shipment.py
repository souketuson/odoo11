from odoo import models, fields, api
from datetime import datetime as dt


class YcShipment(models.Model):
    _name = "yc.shipment"
    name = fields.Char("貨單序號")
    day = fields.Date("出貨日期", default=dt.today())
    acyear = fields.Char("所屬帳款年")
    acmonth = fields.Char("所屬帳款月")
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    pc = fields.Many2one("res.users", string="生管人員", default=lambda self: self.env.user)
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
    factory_id = fields.Many2one("yc.factory", string="所屬工廠", default=lambda self: self.env.user.factory_id)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.user.company_id)

    searchorder = fields.Char("工令")
    searchfurn = fields.Char("爐號")
    searchbuk = fields.Char("桶數")
    searchunit = fields.Many2one("yc.setunit", string="單位")
    searchweight = fields.Char("桶數")
    searchfactory2 = fields.Many2one("yc.processing", string="次加工廠")
    searchcustomer2 = fields.Many2one("yc.customer", "二次廠商")
    searchnote = fields.Text("備註")

    ship_details_ids = fields.One2many("yc.shipment.details", 'name', string="出貨明細檔")

    infurn = fields.Boolean("包含已進爐", default=False)
    verified = fields.Boolean("包含已檢驗", default=False)
    weighted = fields.Boolean("包含已過磅", default=False)
    noshiped = fields.Boolean("不含已出貨", default=False)

    # @api.onchange("searchorder")
    # def search_order(self):
    #     if self.searchorder:
    #         purchase = self.env["yc.purchase"]
    #         order = purchase.search([("name", "=", self.searchorder)])
    #         # furnace爐號所用的欄位 是yc.purchase的order_furn 還是 current_furn?
    #         order_dict = {'order': order.name, 'furnace': order.order_furn.id, "product_code": order.product_code.id,
    #                       'norm_code': order.norm_code.id, 'txtur_code': order.txtur_code.id,
    #                       'buckets': order.weighbuckets,
    #                       'unit': order.unit1.id, 'tweight': order.tweight, 'elecpl_code': order.elecpl_code.id,
    #                       'process1': order.process1.id, 'batch': order.batch, 'fullorhalf': order.fullorhalf,
    #                       'process2': order.process2.id, 'day': order.day, 'wire_furn': order.wire_furn,
    #                       'proces_code': order.proces_code.id,
    #                       }
    #         # 列表待出貨工令
    #         for rec in self:
    #             rec.ship_details_ids = [(0, 0, order_dict)]

    # '依日期變換 貨單序號
    #     Private Sub 出貨日期_ValueChanged(sender As System.Object, e As System.EventArgs) Handles 出貨日期.ValueChanged
    #         If MyTableStatus = 1 Then
    #             strPage = FIRMCODE + Mid(CStr(出貨日期.Value.Year - 1911), 2, 2) + 出貨日期.Value.Month.ToString.PadLeft(2, "0")
    #             '貨單序號.Text = ERP_AutoNo_貨單序號(DNS, strPage, "出貨單主檔", "貨單序號")
    # name = 登入廠 + 民國年尾2位數 + 月份(0x) + 四位數流水號

    @api.model
    def create(self, vals):
        # 新增狀態時會先按wizard button
        day = vals['day']
        user_factory_id = self.env.user.factory_id.id
        firm = self.env['yc.factory'].search([('id', '=', user_factory_id)])
        if firm.name == '岡山廠':
            firm_code = '2'
        else:
            firm_code = ''
        year = int(day[0:4]) - 1911
        month = int(day[5:7])
        ship = self.env["yc.shipment"]
        prefix = str(firm_code) + str(year) + "%02d" % month
        bunch = ship.search([("name","=", prefix)])
        serial = len(bunch) + 1
        name = prefix + '%04d' % serial
        vals.update({'name': name})
        return super(YcShipment, self).create(vals)

    @api.multi
    def write(self, vals):
        # 將取出的工令狀態改成已出貨或已進爐
        # 因為按下待出貨紀錄的wizard button已經跑過一次create() 所以這次要覆寫write()
        # 先看一筆狀況如何
        order = self.env['yc.purchase']
        shipped = self.env['yc.setstatus'].search([('name', '=', '已出貨')])
        if vals.get('ship_details_ids'):
            for list in vals['ship_details_ids']:
                # list 可能是又一層可迭代容器 list[0] = 0 表示項目檔有資料新增
                if hasattr(list, '__iter__') and list[0]==0:
                    for k in list:
                        if hasattr(k, '__iter__') and hasattr(k, 'get'):
                            name = k.get('order')
                            record = order.search([('name','=',name)])
                            # 轉已出貨 & m2o 對應 id
                            record.status = shipped.id
            # 如果刪掉項目檔的東西 狀態轉回已進爐
            # elif hasattr(list, '__iter__') and list[0]==2:
        return super(YcShipment, self).write(vals)


    # 轉待出貨或刪除按鈕
    def toship_or_delete(self):
        # shipment = self.env['yc.shipment.details']
        # check = shipment.search([("ship_check", "=", True)])
        for i in self.ship_details_ids:
            i.ship_check


class YcShipmentDetails(models.Model):
    _name = "yc.shipment.details"
    name = fields.Many2one("yc.shipment", "貨單序號", ondelete='cascade')

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

    @api.multi
    def unlink(self):
        # 如果刪掉項目檔工令 該工令要轉回已進爐狀態
        # 可能多筆
        if self:
            purchase = self.env['yc.purchase']
            infurn = self.env['yc.setstatus'].search([('name', '=', '己進爐')])
            for rec in self:
                order = rec.order
                record = purchase.search([('name','=',order)])
                record.status = infurn.id
        return super(YcShipmentDetails, self).unlink()

# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt
from addons_yc.yc_root.models.weight import YcWeight


class YcPurchase(models.Model):
    _name = "yc.purchase"

    name = fields.Char("工令號碼", default=lambda self: self.env["ir.sequence"].next_by_code("Purchase.sequence"))
    day = fields.Date("日期", default=dt.today())
    time = fields.Char("時間", default=lambda self: YcWeight._get_time(self))
    copy_createdate = fields.Char("製表日期", compute="_fetch_create_date")
    state = fields.Char("狀態")
    weighstate = fields.Char("過磅狀態")
    checkstate = fields.Char("檢驗狀態")
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    factory_id = fields.Many2one("yc.factory", string="所屬工廠")
    processing_attache = fields.Many2one("yc.weight.details", "加工廠名稱")
    processing_phone = fields.Char("加工廠電話")
    processing_contact = fields.Char("負責人")
    combo_process = fields.Char("加工廠聯絡資訊", compute='_compute_process')
    pre_order = fields.Char("前工令號碼")
    car_no = fields.Many2one("yc.weight", string="車次序號")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    customer_phone = fields.Char("客戶電話")
    customer_contact = fields.Char("客戶聯絡人")
    combo_customer = fields.Char("客戶聯絡資訊", compute="_compute_customer")
    batch = fields.Char("客戶批號")
    customer_no = fields.Char("客戶單號")
    person = fields.Many2one("yc.hr", string="開單人員")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    len_code = fields.Many2one("yc.setlength", string="長度")
    len_descript = fields.Char("長度說明")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    surface_code = fields.Many2one("yc.setsurface", string="表面處理")
    elecplswitch = fields.Char("表面處理開關", compute="_switcher")
    elecpl_code = fields.Many2one("yc.setelectroplating", string="電鍍別")
    portage = fields.Selection([('C', '含運費'), ('U', '運費自付')], '運費種類')
    num1 = fields.Integer("數量1")
    unit1 = fields.Many2one("yc.setunit", string="單位代號1")
    num2 = fields.Integer("數量2")
    unit2 = fields.Many2one("yc.setunit", string="單位代號2")
    num3 = fields.Integer("數量3")
    unit3 = fields.Many2one("yc.setunit", string="單位代號3")
    num4 = fields.Integer("數量4")
    unit4 = fields.Many2one("yc.setunit", string="單位代號4")
    storeplace = fields.Char("存放位置")
    net = fields.Char("淨重")
    process1 = fields.Many2one("yc.processing", "次加工廠")
    process2 = fields.Many2one("yc.processing", "二次加工")
    totalpack = fields.Char("裝袋合計")
    standard = fields.Char("依據標準")
    wire_furn = fields.Char("線材爐號")

    headsign = fields.Binary('頭部記號')

    surfhrd = fields.Char("表面硬度")
    corehrd = fields.Char("心部硬度")
    piece = fields.Selection([('Y', '是'), ('N', '否')], '試片')
    tensihrd = fields.Char("抗拉強度")
    carburlayer = fields.Char("滲碳層")
    torsion = fields.Char("扭力")
    retempt = fields.Char("回火溫度")
    pre_furn = fields.Char("以前爐號")
    order_furn = fields.Char("預排爐號")
    norcls = fields.Char("規範分類")
    wxr_txtur = fields.Char("華司材質")
    wxrhard = fields.Char("華司硬度")
    fullorhalf = fields.Selection([('H', '半牙'), ('F', '全牙'), ('N', '無')], '全或半牙')

    notices1 = fields.Char("注意事項1")
    notices2 = fields.Char("注意事項2")
    notices3 = fields.Char("注意事項3")
    notices4 = fields.Char("注意事項4")
    qcnote1 = fields.Char("品管備註1")
    qcnote2 = fields.Char("品管備註2")
    qcnote3 = fields.Char("品管備註3")
    prodnote1 = fields.Char("製造備註1")
    prodnote2 = fields.Char("製造備註2")
    prodnote3 = fields.Char("製造備註3")

    # 作業條件page
    flow = fields.Char("流量")
    cp = fields.Char("CP值")
    nh31 = fields.Char("氨值1")
    nh32 = fields.Char("氨值2")
    nh33 = fields.Char("氨值3")
    nh34 = fields.Char("氨值4")

    heat1 = fields.Char("加熱爐1")
    heat2 = fields.Char("加熱爐2")
    heat3 = fields.Char("加熱爐3")
    heat4 = fields.Char("加熱爐4")
    heat5 = fields.Char("加熱爐5")
    heat6 = fields.Char("加熱爐6")
    heat7 = fields.Char("加熱爐7")
    heat8 = fields.Char("加熱爐8")

    heattemp = fields.Char("加熱爐油溫")
    heatsped = fields.Char("加熱爐速度")
    tempturing1 = fields.Char("回火爐1")
    tempturing2 = fields.Char("回火爐2")
    tempturing3 = fields.Char("回火爐3")
    tempturing4 = fields.Char("回火爐4")
    tempturing5 = fields.Char("回火爐5")
    tempturing6 = fields.Char("回火爐6")
    tempturisped = fields.Char("回火爐速度")

    @api.one
    @api.depends('processing_attache')
    def _compute_process(self):
        if self.processing_attache:
            for rec in self:
                self.combo_process = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.processing_id.phone, self.processing_attache.processing_id.contact)
                self.combo_customer = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.customer_id.phone, self.processing_attache.customer_id.contact)
                self.customer_id = self.processing_attache.customer_id.id

    @api.model
    def _fetch_create_date(self):
        self.copy_createdate = self.create_date[:10]

    # 1.過濾該天幾張過磅單 並在car_no fields 顯示 該天單號之車次序號
    @api.onchange("day")
    def _filter_car_no(self):
        return {'domain': {"car_no": [("day", "=", self.day)]}}

    # 2.填完車次序號 自動帶出該次司機
    @api.onchange("car_no")
    def _driver_id(self):
        for rec in self:
            rec.driver_id = self.car_no.driver_id.id

    # 3.選完車次序號 篩選出該車次之加工廠(找單號)
    @api.onchange("car_no")
    def _filter_processing(self):
        # 這裡 self.car_no.id 是該車次的過磅單號
        return {'domain': {"processing_attache": [("name", "=", self.car_no.id)]}}

    # @api.onchange('processing_attache')
    # def _get_number_name(self):
    #     if self.processing_attache:
    #         for rec in self:
    #             self.combo_process = "電話: " + self.processing_attache.processing_id.phone + '   聯絡人:' + self.processing_attache.processing_id.contact
    #             rec.combo_process = self.combo_process

    # 4. 選完加工廠自動返回該項目客戶
    # @api.onchange("processing_attache")
    # def _customer_id(self):
    #     if self.processing_attache:
    #         for rec in self:
    #             self.customer_id = rec.env["yc.weight.details"].search(
    #                 [("id", "=", rec.processing_attache.id)]).customer_id.id
    #             customer = self.env["yc.customer"].search([("id", "=", self.customer_id.id)])
    #             self.combo_customer = "電話: " + customer.phone + '   聯絡人: ' + customer.contact
    #             return {"domain": {"customer_id": [("name", "=", rec.car_no.id)]}}

    # 覆寫新增資料:create()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有create方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    # @api.model
    # def create(self, vals):
    # 針對 processing_phone 、 processing_contact&customer_id 的新增資料寫法
    # processing = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).processing_id.id
    # vals["processing_phone"] = self.env["yc.processing"].search([("id", "=", processing)]).phone
    # vals["processing_contact"] = self.env["yc.processing"].search([("id", "=", processing)]).contact

    # customer = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).customer_id.id
    # vals["customer_id"] = self.env["yc.customer"].search([("id", "=", customer)]).id
    # return super(YcPurchase, self).create(vals)

    # 覆寫新增資料:write()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有write方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    # @api.multi
    # def write(self, vals):
    #     # 針對 processing_phone & processing_contact 的修改資料寫法
    #     # Issue: 進編輯畫面 refresh day的資訊觸發onchange 否則資訊會無法啟動過濾機制
    #     if vals.get('processing_attache'):
    #         shift_processing = vals['processing_attache']
    #         processing_id = self.env['yc.weight.details'].search([('id', '=', shift_processing)]).processing_id.id
    #         customer = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).customer_id.id
    #         vals['processing_phone'] = self.env['yc.processing'].search([('id', '=', processing_id)]).phone
    #         vals['processing_contact'] = self.env['yc.processing'].search([('id', '=', processing_id)]).contact
    #         vals["customer_id"] = self.env["yc.customer"].search([("id", "=", customer)]).id

    # return super(YcPurchase, self).write(vals)

    # 品名分類(clsf_code)以及規格(norm_code)帶出 1.依據標準 2.表面硬度 3.心部硬度 4.試片 5.抗拉強度 6.扭力
    # 以norm_code 的 parameter1值 去搜尋落在 產品機械性質主檔的 規格代碼起迄內之資料
    # ! 舊資料庫 一層代碼的S03N0004 規格 裡面參數1資料不乾淨 造成查詢資料出現bug 須提供新的資料
    # ?怪怪的 select * from 產品機械性質主檔 a WHERE a.產品分類代號 = 品名分類代碼.SelectedValue \
    #  and a.強度級數 = 強度級數.SelectedValue \
    #  and CAST(a.規格對照起 AS float) <=" + 直徑規格數字.ToString \
    #  and CAST(a.規格對照迄 AS float) >=" + 直徑規格數字.ToString \

    # select * from 扭力規格主檔 a
    # WHERE a.品名分類= 品名分類代碼.SelectedValue
    # and a.強度級數= 強度級數.SelectedValue
    # and a.直徑規格= 規格代碼.SelectedValue
    @api.onchange("norm_code", "clsf_code")
    def _fetch_norm_code_info(self):
        if self.norm_code and self.clsf_code:
            for rec in self:
                norm_parameter = rec.env["yc.setnorm"].search([('id', '=', rec.norm_code.id)]).parmeter1
                # 如果有強度
                mechaine_name = rec.env["yc.mechanicalproperty"].search( \
                    [('clsf_code', '=', rec.clsf_code.id), ("strength_level", "=", rec.strength_level.id), \
                     ('stdreviewinit', '<=', norm_parameter), ('stdreviewend', '>=', norm_parameter)])
                torsion_name = rec.env["yc.torsion"].search(
                    [('clsf_code', '=', rec.clsf_code.id), ("strength_level", "=", rec.strength_level.id),
                     ("norm_code", "=", rec.norm_code.id)])
                if bool(mechaine_name):
                    self.standard = mechaine_name.standard
                    self.surfhrd = mechaine_name.innersurfhrd
                    self.corehrd = mechaine_name.innercorehrd
                    self.tensihrd = mechaine_name.innertensihrd
                    self.carburlayer = mechaine_name.innercarburlayer
                    self.torsion = torsion_name.torsion1
                elif bool(mechaine_name) == False and bool(rec.clsf_code and rec.strength_level) == True:
                    # self.standard = None
                    # self.surfhrd = None
                    # self.corehrd = None
                    # self.tensihrd = None
                    # self.carburlayer = None

                    # 只有異動完規格(norm_code)才會跳檢查
                    return {
                        'warning': {
                            'title': '提醒',
                            'message': '沒有這個機械性質分類'}
                    }

    # 當表面處理開啟'電鍍'時，啟用電鍍類別
    @api.onchange("surface_code")
    def _switcher(self):
        for rec in self:
            if rec.surface_code.id == 4:
                self.elecplswitch = 'ON'
                self.elecpl_code = 538
            elif rec.surface_code.id == 2:
                self.elecpl_code = 385
            elif rec.surface_code.id == 1:
                self.elecpl_code = 590
            else:
                # 避免非電鍍類別存入資料
                self.elecplswitch = 'OFF'
                rec.elecpl_code = None

    # 裝袋合計合計處理
    @api.onchange("num1", "num2", "num3", "num4")
    def _count_bag(self):
        self.totalpack = (self.num1 or 0)+(self.num2 or 0)+(self.num3 or 0)+(self.num4 or 0)

    # 邊在輸入進貨資料時，系統就會一邊在幫我們蒐尋舊資料,品名分類、品名、強度級數、材質、規格、加工方式、線材爐號
    @api.onchange("clsf_code", "product_code", "strength_level", "txtur_code", "norm_code", "proces_code", "wire_furn")
    def _search_process_condition(self):
        if self.clsf_code and self.product_code and self.strength_level and self.txtur_code and self.norm_code and self.proces_code and self.wire_furn:
            _filter = self.env["yc.purchase"].search(
                [("clsf_code", "=", self.clsf_code.id), ("product_code", "=", self.product_code.id), \
                 ("strength_level", "=", self.strength_level.id), ("txtur_code", "=", self.txtur_code.id), \
                 ("norm_code", "=", self.norm_code.id), ("proces_code", "=", self.proces_code.id), \
                 ("wire_furn", "=", self.wire_furn)], limit=1, order='id DESC')

            self.flow = _filter.flow
            self.cp = _filter.cp
            self.nh31 = _filter.nh31
            self.nh32 = _filter.nh32
            self.nh33 = _filter.nh33
            self.nh34 = _filter.nh34
            self.heat1 = _filter.heat1
            self.heat2 = _filter.heat2
            self.heat3 = _filter.heat3
            self.heat4 = _filter.heat4
            self.heat5 = _filter.heat5
            self.heat6 = _filter.heat6
            self.heat7 = _filter.heat7
            self.heat8 = _filter.heat8
            self.heattemp = _filter.heattemp
            self.heatsped = _filter.heatsped
            self.tempturing1 = _filter.tempturing1
            self.tempturing2 = _filter.tempturing2
            self.tempturing3 = _filter.tempturing3
            self.tempturing4 = _filter.tempturing4
            self.tempturing5 = _filter.tempturing5
            self.tempturing6 = _filter.tempturing6
            self.tempturisped = _filter.tempturisped


class YcSetproduct(models.Model):
    # 產品資料 S03N0001
    _name = "yc.setproduct"
    name = fields.Char("產品名稱")
    code = fields.Char("產品代碼")

    @api.multi
    def name_get(self):
        return [(record.id, "%s %s" % (record.code, record.name)) for record in self]

    # 讓many2one下拉可以搜尋"代碼"來找產品
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if u'\u4e00' <= name <= u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = ['|', ('code', operator, name), ('name', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()


class YcPurchaseStore(models.Model):
    _name = "yc.purchasestore"

    name = fields.Char("進貨庫存單號")


class YcPurchaseStore(models.Model):
    _name = "yc.purchasereport"

    name = fields.Char("客戶進貨統計表")

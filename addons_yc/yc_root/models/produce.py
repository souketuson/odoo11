# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools import image
from datetime import datetime as dt


class YcWeight(models.Model):
    _name = "yc.weight"

    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    name = fields.Char("過磅單號", default=lambda self: self.env["ir.sequence"].next_by_code("WeightList.sequence"))
    day = fields.Date("過磅日期", default=dt.today())
    weightime = fields.Char("過磅時間", default=lambda self: self._get_time())
    person_id = fields.Many2one("yc.hr", string="過磅員")
    weighbridge = fields.Char("地磅序號")
    carno = fields.Char("車次序號")
    in_out = fields.Selection([('I', '進貨'), ('O', '出貨')], '進出貨')
    factory_id = fields.Many2one("yc.factory", string="所屬工廠")
    purchase_times = fields.Integer("進貨次數")
    ship_times = fields.Integer("出貨次數")
    plate_no = fields.Char("車號", related="driver_id.plate_no")
    total = fields.Integer("總重 (KG)")
    curbweight = fields.Integer("空車重 (KG)")
    emptybucket = fields.Integer("空桶重 (KG)")
    net = fields.Integer("淨重 (KG)")
    note = fields.Char("備註")
    refine = fields.Integer("調質重量 (KG)")
    carbur = fields.Integer("滲碳重量")
    other = fields.Integer("其他重量 (KG)")
    other1 = fields.Integer("其他重量1")
    count = fields.Integer("貨重(應等於淨重)", compute="_check_weight")
    # 一張過磅單 上面的貨物可能含有多家客戶
    customer_detail_ids = fields.One2many("yc.weight.details", "name", "客戶明細")

    # 要改成自動編號 & 上鎖
    # @api.multi
    # @api.onchange("name")
    # def _generate(self):
    #     '''WL + 190227 + 001...999
    #                 2    +  6          + 3
    #
    #                 '''
    #     # prefix WL + yymmdd
    #     _serial = 'WL' + dt.today().strftime("%y%m%d")
    #     # search today's last one data on db
    #     obj = self.env['yc.weight'].search([('name', '=like', _serial + "%")], limit=1, order='name DESC')
    #     if obj:  # 如果無/有系列碼
    #         _next = int(obj[0].name[8:]) + 1
    #         _serial += '%03d' % _next
    #     else:
    #         _serial += '001'
    #     self.name = _serial

    @api.model
    def _get_time(self):
        # 不知道為什麼 odoo 有時候會把datetime.now()的時間丟到頁面後會 -8小時
        # 有以上狀況 hour +8 即可解決
        hour = dt.now().hour + 8
        minute = dt.now().minute
        sec = dt.now().second
        if hour > 24:
            hour -= 24

        time = "%02d:%02d:%02d" % (hour, minute, sec)
        return time

    # 車次序號產生
    @api.multi
    @api.onchange("driver_id")
    def _generate_carno(self):
        for rec in self:
            if rec.driver_id:
                year = str(dt.now().year)
                month = "%02d" % (dt.now().month)
                day = "%02d" % (dt.now().day)
                # S1
                if year[3:] == "0":
                    S1 = "A"
                elif year[3:] == "1":
                    S1 = "B"
                elif year[3:] == "2":
                    S1 = "C"
                elif year[3:] == "3":
                    S1 = "D"
                else:
                    S1 = year[3:]

                # S2
                if month == "10":
                    S2 = "A"
                elif month == "11":
                    S2 = "B"
                elif month == "12":
                    S2 = "C"
                else:
                    S2 = month[1:]

                # S3
                day_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                            'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
                S3 = day_list[int(day) - 1]

                # S4 S5

                S4 = rec.env["yc.driver"].search([('name', '=', rec.driver_id.name)]).code

                check_day = dt.strptime(rec.day, "%Y-%m-%d")
                check = rec.env["yc.weight"].search([('driver_id', '=', rec.driver_id.name), ('day', '=', check_day)])
                if check:
                    S5 = str(len(check) + 1)
                else:
                    S5 = "1"

                if S1 and S2 and S3 and S4 and S5:
                    self.carno = str(S1 + S2 + S3 + S4 + S5)
                    rec.carno = self.carno

    # 檢查進出貨分類是否填寫
    @api.constrains("in_out")
    def _verify(self):
        if not self.in_out:
            raise Warning("進出貨分類空值")

    # 進出貨次數自動計算
    @api.multi
    @api.onchange('in_out')
    def _count(self):
        for rec in self:
            check_day = dt.strptime(rec.day, "%Y-%m-%d")
            pn = self.plate_no
            check_in = self.env["yc.weight"].search(
                [('in_out', '=', 'I'), ('day', '=', check_day), ('plate_no', '=', pn)])
            check_out = self.env["yc.weight"].search(
                [('in_out', '=', 'O'), ('day', '=', check_day), ('plate_no', '=', pn)])

            # 判斷新建還是修改 看單號有沒有在資料庫
            if rec.in_out:  # 進出貨有值
                if pn and rec.day:  # 車牌&日期 有值
                    self.ship_times = len(check_out)
                    self.purchase_times = len(check_in)
                    if not self.env["yc.weight"].search([("name", "=", self.name)]):
                        if rec.in_out == 'I':
                            rec.ship_times = self.ship_times
                            rec.purchase_times = self.purchase_times + 1
                        elif rec.in_out == 'O':
                            # onchange decorator 要存到db 需要rec.field = self.field 這種寫法
                            rec.ship_times = self.ship_times + 1
                            rec.purchase_times = self.purchase_times

    # 選完司機名稱，車牌自動帶入 > 改用related 取代
    # @api.multi
    # @api.onchange("driver_id")
    # def _auto_fetch_plateno(self):
    #     for rec in self:
    #         if self.driver_id:
    #             self.plate_no = self.env["yc.driver"].search([('name', '=', rec.driver_id.name)]).plate_no
    #             rec.plate_no = self.plate_no
    #         else:
    #             pass

    # 淨重自動計算
    @api.onchange("total", "curbweight", "emptybucket")
    def _NetWeight(self):
        self.net = self.total - self.emptybucket - self.curbweight

    # 覆寫新增資料:create()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有create方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    @api.model
    def create(self, vals):
        _net = vals["total"] - vals["emptybucket"] - vals["curbweight"]
        vals.update({"net": _net})
        return super(YcWeight, self).create(vals)

    # 覆寫修改資料:write()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有write方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    @api.multi
    def write(self, vals):
        # 沒有修改 vals(dict)就沒有值
        # 如果沒有值 就等於self 如果有值就沿用
        _net_parameter = ["total", "curbweight", "emptybucket"]
        for key in _net_parameter:
            if key in vals:
                pass
            else:
                vals[key] = self[key]
        _net = vals["total"] - vals["emptybucket"] - vals["curbweight"]
        vals.update({"net": _net})
        return super(YcWeight, self).write(vals)

    # 檢查淨重是否等於貨重
    @api.constrains("refine", "carbur", "other", "other1")
    def _verify_weight(self):
        total = self.refine + self.carbur + self.other + self.other1
        if self.net and total != self.net:
            raise Warning("調質重量+滲碳單價+其他重量+其他重量1 應等於 淨重")
        else:
            pass

    # 貨重計算(調值、滲碳、其他、其他1)
    @api.onchange("refine", "carbur", "other", "other1")
    def _check_weight(self):
        total = self.refine + self.carbur + self.other + self.other1
        self.count = total

    # many2one這個資料庫時 會用這裡的name 而不是(name)單號
    # 和 _rec_name = "carno" 一樣效果
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.carno
            result.append((record.id, name))
        return result


class YcWeightDetails(models.Model):
    _name = "yc.weight.details"

    name = fields.Many2one("yc.weight", "訂單編號", ondelete="cascade")
    no = fields.Integer("序號")
    max_sequence = fields.Integer(string="最大數", compute="_get_sequence")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    processing_id = fields.Many2one("yc.processing", "加工廠名稱")
    note = fields.Char("備註")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            processing = record.env['yc.processing'].search([('code', '=', record.processing_id.code)])
            name = processing.name
            result.append((record.id, name))
        return result

    # 新增刪除時 更新sequence數量
    @api.onchange()
    def _get_sequnce(self):
        pass

    # max_no = fields.Integer(help="最大項目數",default=lambda self: self._max_no())
    # @api.multi
    # @api.onchange("max_no")
    # def _max_no(self):
    #
    #     for detail in self:
    #         _name = detail.name_get()[0][1]
    #         detail.max_no = len(detail.env["yc.weight.details"].search([('name', '=', _name)])) + 1
    #
    #
    # @api.model
    # def create(self, vals):
    #     vals.update({"no": self.max_no + 1})
    #     return super(YcWeightDetails, self).create(vals)


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
    combo_process = fields.Char("加工廠聯絡資訊")
    pre_order = fields.Char("前工令號碼")
    car_no = fields.Many2one("yc.weight", string="車次序號")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    customer_phone = fields.Char("客戶電話")
    customer_contact = fields.Char("客戶聯絡人")
    combo_customer = fields.Char("客戶聯絡資訊")
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

    # domainlist = fields.Char()

    # 加工廠電話、負責人攜出
    # @api.onchange("processing_id")
    # def _fetch_processing_info(self):
    #     for rec in self:
    #         processing = rec.env["yc.processing"].search([("id", "=", rec.processing_id.id)])
    #         self.processing_phone = processing.phone
    #         rec.processing_phone = self.processing_phone
    #
    # def _fetch_date(self):
    #     if self.day:
    #         self.day = self.day

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

    @api.onchange('processing_attache')
    def _get_number_name(self):
        if self.processing_attache:
            for rec in self:
                self.combo_process = "電話: " + self.processing_attache.processing_id.phone + '   聯絡人:' + self.processing_attache.processing_id.contact
                rec.combo_process = self.combo_process

    # self.combo_customer = "電話: " + self.env["yc.customer"].search("id", "=", self.customer_id).phone + '  聯絡人: ' + \
    #                       self.env["yc.customer"].search("id", "=", self.customer_id).contact

    # 4. 選完加工廠自動返回該項目客戶
    @api.onchange("processing_attache")
    def _customer_id(self):
        if self.processing_attache:
            for rec in self:
                self.customer_id = rec.env["yc.weight.details"].search(
                    [("id", "=", rec.processing_attache.id)]).customer_id.id
                customer = self.env["yc.customer"].search([("id", "=", self.customer_id.id)])
                self.combo_customer = "電話: " + customer.phone + '   聯絡人: ' + customer.contact
                return {"domain": {"customer_id": [("name", "=", rec.car_no.id)]}}

    # 覆寫新增資料:create()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有create方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    @api.model
    def create(self, vals):
        # 針對 processing_phone 、 processing_contact&customer_id 的新增資料寫法
        processing = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).processing_id.id
        customer = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).customer_id.id
        vals["processing_phone"] = self.env["yc.processing"].search([("id", "=", processing)]).phone
        vals["processing_contact"] = self.env["yc.processing"].search([("id", "=", processing)]).contact
        vals["customer_id"] = self.env["yc.customer"].search([("id", "=", customer)]).id
        return super(YcPurchase, self).create(vals)

    # 覆寫新增資料:write()
    # onchange 裝飾中的函式資料是在虛擬record中，在odoo原有write方法中，參數vals抓不到這些onchange所裝飾的函式資料，所以無法存進資料庫
    @api.multi
    def write(self, vals):
        # 針對 processing_phone & processing_contact 的修改資料寫法
        # Issue: 進編輯畫面 refresh day的資訊觸發onchange 否則資訊會無法啟動過濾機制
        if vals.get('processing_attache'):
            shift_processing = vals['processing_attache']
            processing_id = self.env['yc.weight.details'].search([('id', '=', shift_processing)]).processing_id.id
            customer = self.env["yc.weight.details"].search([("id", "=", vals['processing_attache'])]).customer_id.id
            vals['processing_phone'] = self.env['yc.processing'].search([('id', '=', processing_id)]).phone
            vals['processing_contact'] = self.env['yc.processing'].search([('id', '=', processing_id)]).contact
            vals["customer_id"] = self.env["yc.customer"].search([("id", "=", customer)]).id

        return super(YcPurchase, self).write(vals)

    # 品名分類(clsf_code)以及規格(norm_code)帶出 1.依據標準 2.表面硬度 3.心部硬度 4.試片 5.抗拉強度 6.扭力
    # 以norm_code 的 parameter1值 去搜尋落在 產品機械性質主檔的 規格代碼起迄內之資料
    # ! 舊資料庫 一層代碼的S03N0004 規格 裡面參數1資料不乾淨 造成查詢資料出現bug 須提供新的資料
    # ?怪怪的 select * from 產品機械性質主檔 a WHERE a.產品分類代號 = 品名分類代碼.SelectedValue \
    #  and a.強度級數 = 強度級數.SelectedValue \
    #  and CAST(a.規格對照起 AS float) <=" + 直徑規格數字.ToString \
    #  and CAST(a.規格對照迄 AS float) >=" + 直徑規格數字.ToString \
    @api.onchange("norm_code")
    def _fetch_norm_code_info(self):
        for rec in self:
            norm_parameter = rec.env["yc.setnorm"].search([('id', '=', rec.norm_code.id)]).parmeter1
            # 如果有強度
            mechaine_name = rec.env["yc.mechanicalproperty"].search( \
                [('clsf_code', '=', rec.clsf_code.id), ("strength_level", "=", rec.strength_level.id), \
                 ('stdreviewinit', '<=', norm_parameter), ('stdreviewend', '>=', norm_parameter)])
            if bool(mechaine_name):
                self.standard = mechaine_name.standard
                self.surfhrd = mechaine_name.innersurfhrd
                self.corehrd = mechaine_name.innercorehrd
                self.tensihrd = mechaine_name.innertensihrd
                self.carburlayer = mechaine_name.innercarburlayer
            elif bool(mechaine_name) == False and bool(rec.clsf_code and rec.strength_level) == True:
                # self.standard = None
                # self.surfhrd = None
                # self.corehrd = None
                # self.tensihrd = None
                # self.carburlayer = None
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
            else:
                # 避免非電鍍類別存入資料
                self.elecplswitch = 'OFF'
                rec.elecpl_code = None

    # 裝袋合計合計處理
    # 邊在輸入進貨資料時，系統就會一邊在幫我們蒐尋舊資料,品名分類、品名、強度級數、材質、規格、加工方式、線材爐號


class YcSetproduct(models.Model):
    # 產品資料 S03N0001
    _name = "yc.setproduct"
    name = fields.Char("產品名稱")
    code = fields.Char("產品代碼")

    @api.multi
    def name_get(self):
        return [(record.id, "%s %s" % (record.code, record.name)) for record in self]

    # @api.multi
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         name = record.code + ' ' + record.name
    #         res.append((record.id, record.code, name))
    #     return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if u'\u4e00' <= name <= u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = ['|', ('code', operator, name), ('name', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()


class YcSetstrength(models.Model):
    # 強度級數 S03N0002
    _name = "yc.setstrength"
    name = fields.Char("強度名稱")
    code = fields.Char("強度代碼")


class YcSetproductclassify(models.Model):
    # 產品分類 S03N0003
    _name = "yc.setproductclassify"
    name = fields.Char("分類名稱")
    code = fields.Char("分類代碼")


class YcSetnorm(models.Model):
    # 規格 S03N0004
    _name = "yc.setnorm"
    name = fields.Char("規格名稱")
    code = fields.Char("規格代碼")
    parmeter1 = fields.Char("參數1")
    parmeter2 = fields.Char("參數2")
    parmeter3 = fields.Char("參數3")


class YcSetlength(models.Model):
    # 長度 S03N0005
    _name = "yc.setlength"
    name = fields.Char("長度名稱")
    code = fields.Char("長度代碼")


class YcSetprocess(models.Model):
    #  加工方式 S03N0006
    _name = "yc.setprocess"
    name = fields.Char("加工方式")
    code = fields.Char("加工方式代碼")


class YcSettexture(models.Model):
    # 材質 S03N0007
    _name = "yc.settexture"
    name = fields.Char("材質名稱")
    code = fields.Char("材質代碼")


class YcSetsurface(models.Model):
    # 表面處理 S03N0008
    _name = "yc.setsurface"
    name = fields.Char("表面處理名稱")
    code = fields.Char("表面處理代碼")


class YcSetelectroplating(models.Model):
    # 電鍍 S03N0009
    _name = "yc.setelectroplating"
    name = fields.Char("電鍍名稱")
    code = fields.Char("電鍍代碼")


class YcSeteunit(models.Model):
    # 單位 S03N0011
    _name = "yc.setunit"
    name = fields.Char("單位名稱")
    code = fields.Char("單位代碼")


class YcPurchaseStore(models.Model):
    _name = "yc.purchasestore"

    name = fields.Char("進貨庫存單號")


class YcPurchaseStore(models.Model):
    _name = "yc.purchasereport"

    name = fields.Char("客戶進貨統計表")

# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt
import collections


class YcPurchase(models.Model):
    _name = "yc.purchase"

    name = fields.Char("工令號碼")

    def _default_name(self):
        if self._context.get('params')['action'] == 81:
            # 車次序號 + 01~99
            pass
            # return self.env["ir.sequence"].next_by_code("Purchase.sequence")

    day = fields.Date("進貨日期", default=lambda self: self._default_date())

    def _default_date(self):
        if self._context.get('params')['action'] == 81:
            return dt.today()

    time = fields.Char("時間", default=lambda self: self._get_time())
    copy_createdate = fields.Char("製表日期", compute="_fetch_create_date")
    status = fields.Many2one("yc.setstatus", string="狀態", default=2)
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
    combo_customer = fields.Char("客戶聯絡資訊")
    batch = fields.Char("客戶批號")
    customer_no = fields.Char("客戶單號")
    person = fields.Many2one("yc.hr", string="開單人員")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    product_id = fields.Char("品名代碼")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    len_code = fields.Many2one("yc.setlength", string="長度")
    # 待確定
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
    net = fields.Integer("淨重")
    process1 = fields.Many2one("yc.processing", "次加工廠")
    process2 = fields.Many2one("yc.processing", "二次加工")
    totalpack = fields.Char("裝袋合計")
    standard = fields.Char("依據標準")
    wire_furn = fields.Char("線材爐號")

    headsign = fields.Binary('頭部記號')

    surfhrd = fields.Char("表面硬度")
    corehrd = fields.Char("心部硬度")
    piece = fields.Selection([('Y', '是'), ('N', '否')], '試片')
    carburlayer = fields.Char("滲碳層")
    torsion = fields.Char("扭力")
    retempt = fields.Integer("回火溫度")
    pre_furn = fields.Char("以前爐號")
    # 0517設成Many2one 轉檔要抓id 不能直接匯入
    order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
    norcls = fields.Char("規範分類")
    wxr_txtur = fields.Char("華司材質")
    wxrhard = fields.Char("華司硬度")
    fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')

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
    furnstat = fields.Char("進爐狀態")
    produceday = fields.Date("製造日期")
    ptime = fields.Char("製造時間")
    op = fields.Many2one("yc.hr", string="操作人員")
    qc = fields.Many2one("yc.hr", string="品管人員")
    shift = fields.Many2one("yc.setshift", string="班別")
    ssk = fields.Float("斷面積")
    mxload1 = fields.Float("最大負荷1")
    mxload2 = fields.Float("最大負荷2")
    mxload3 = fields.Float("最大負荷3")
    mxload4 = fields.Float("最大負荷4")
    mxload5 = fields.Float("最大負荷5")
    mxload6 = fields.Float("最大負荷6")
    mxload7 = fields.Float("最大負荷7")
    mxload8 = fields.Float("最大負荷8")

    yield1 = fields.Float("降伏點值1")
    yield2 = fields.Float("降伏點值2")
    yield3 = fields.Float("降伏點值3")
    yield4 = fields.Float("降伏點值4")
    yield5 = fields.Float("降伏點值5")
    yield6 = fields.Float("降伏點值6")
    yield7 = fields.Float("降伏點值7")
    yield8 = fields.Float("降伏點值8")

    elong1 = fields.Float("伸長率值1")
    elong2 = fields.Float("伸長率值2")
    elong3 = fields.Float("伸長率值3")
    elong4 = fields.Float("伸長率值4")
    elong5 = fields.Float("伸長率值5")
    elong6 = fields.Float("伸長率值6")
    elong7 = fields.Float("伸長率值7")
    elong8 = fields.Float("伸長率值8")

    decarb1 = fields.Float("脫碳層值1")
    decarb2 = fields.Float("脫碳層值2")
    decarb3 = fields.Float("脫碳層值3")
    decarb4 = fields.Float("脫碳層值4")
    decarb5 = fields.Float("脫碳層值5")
    decarb6 = fields.Float("脫碳層值6")
    decarb7 = fields.Float("脫碳層值7")
    decarb8 = fields.Float("脫碳層值8")

    wxrhrd1 = fields.Float("華司硬度值1")
    wxrhrd2 = fields.Float("華司硬度值2")
    wxrhrd3 = fields.Float("華司硬度值3")
    wxrhrd4 = fields.Float("華司硬度值4")
    wxrhrd5 = fields.Float("華司硬度值5")
    wxrhrd6 = fields.Float("華司硬度值6")
    wxrhrd7 = fields.Float("華司硬度值7")
    wxrhrd8 = fields.Float("華司硬度值8")

    icritetia = fields.Char("國際標準")
    tensile_no = fields.Selection([('50T', '50T'), ('100T', '100T')], '拉力機編號')
    # 轉檔要修成id
    sfhn = fields.Many2one("yc.sethardness", string="表面硬度規格")
    sfhv = fields.Char("表面硬度值")
    sfhv1 = fields.Float("表面硬度值1")
    sfhv2 = fields.Float("表面硬度值2")
    sfhv3 = fields.Float("表面硬度值3")
    sfhv4 = fields.Float("表面硬度值4")
    sfhv5 = fields.Float("表面硬度值5")
    sfhv6 = fields.Float("表面硬度值6")
    sfhv7 = fields.Float("表面硬度值7")
    sfhv8 = fields.Float("表面硬度值8")
    # 轉檔要修成id
    chn = fields.Many2one("yc.sethardness", string="心部硬度規格")
    chv = fields.Char("心部硬度值")
    chv1 = fields.Float("心部硬度值1")
    chv2 = fields.Float("心部硬度值2")
    chv3 = fields.Float("心部硬度值3")
    chv4 = fields.Float("心部硬度值4")
    chv5 = fields.Float("心部硬度值5")
    chv6 = fields.Float("心部硬度值6")
    chv7 = fields.Float("心部硬度值7")
    chv8 = fields.Float("心部硬度值8")

    tensihrd = fields.Char("抗拉強度")
    rtens = fields.Char("抗拉強度值")
    # tensihrd 和 rtens 這兩者不知道有哪邊不一樣?
    rtenste = fields.Char("抗拉強度值起迄", default=lambda self: self._get_rtenste())

    resist1 = fields.Float("抗拉強度值1")
    resist2 = fields.Float("抗拉強度值2")
    resist3 = fields.Float("抗拉強度值3")
    resist4 = fields.Float("抗拉強度值4")
    resist5 = fields.Float("抗拉強度值5")
    resist6 = fields.Float("抗拉強度值6")
    resist7 = fields.Float("抗拉強度值7")
    resist8 = fields.Float("抗拉強度值8")

    # @api.depends("rtenste")
    def _get_rtenste(self):
        for rec in self:
            rt_arr = [rec.resist1, rec.resist2, rec.resist3, rec.resist4, rec.resist5, rec.resist6, rec.resist7,
                      rec.resist8]
            if len(rt_arr) >= 2:
                rt_arr.sort
                rec.rtenste = str(rt_arr[0]) + '~' + str(rt_arr[len(rt_arr) - 1])

    @api.onchange('name')
    def _get_tensihrd_data(self):
        pass

    ysv = fields.Float("降伏強度值")
    ysvste = fields.Char("降伏強度值起迄", default=lambda self: self._get_ysvste())
    ystrength1 = fields.Float("降伏強度值1")
    ystrength2 = fields.Float("降伏強度值2")
    ystrength3 = fields.Float("降伏強度值3")
    ystrength4 = fields.Float("降伏強度值4")
    ystrength5 = fields.Float("降伏強度值5")
    ystrength6 = fields.Float("降伏強度值6")
    ystrength7 = fields.Float("降伏強度值7")
    ystrength8 = fields.Float("降伏強度值8")

    def _get_ysvste(self):
        for rec in self:
            ysv_arr = [rec.ystrength1, rec.ystrength2, rec.ystrength3, rec.ystrength4, rec.ystrength5, rec.ystrength6,
                       rec.ystrength7, rec.ystrength8]
            if len(ysv_arr) >= 2:
                ysv_arr.sort()
                rec.ysvste = str(ysv_arr[0]) + '~' + str(ysv_arr[len(ysv_arr) - 1])

    elohv = fields.Float("伸長率值")
    elohvste = fields.Char("伸長率值起迄")
    yste = fields.Char("降伏點值起迄")
    mxloadste = fields.Char("最大負荷值起迄")
    sskste = fields.Float("斷面積值起迄")
    torshv = fields.Float("扭力強度值")
    torshv1 = fields.Float("扭力強度值1")
    torshv2 = fields.Float("扭力強度值2")
    torshv3 = fields.Float("扭力強度值3")
    torshv4 = fields.Float("扭力強度值4")
    torshv5 = fields.Float("扭力強度值5")
    torshv6 = fields.Float("扭力強度值6")
    torshv7 = fields.Float("扭力強度值7")
    torshv8 = fields.Float("扭力強度值8")

    carb1v = fields.Char("滲碳層1值")
    carb1v1 = fields.Float("滲碳層1值1")
    carb1v2 = fields.Float("滲碳層1值2")
    carb1v3 = fields.Float("滲碳層1值3")
    carb1v4 = fields.Float("滲碳層1值4")
    carb1v5 = fields.Float("滲碳層1值5")
    carb1v6 = fields.Float("滲碳層1值6")
    carb1v7 = fields.Float("滲碳層1值7")
    carb1v8 = fields.Float("滲碳層1值8")

    carb2v1 = fields.Float("滲碳層2值1")
    carb2v2 = fields.Float("滲碳層2值2")
    carb2v3 = fields.Float("滲碳層2值3")
    carb2v4 = fields.Float("滲碳層2值4")
    carb2v5 = fields.Float("滲碳層2值5")
    carb2v6 = fields.Float("滲碳層2值6")
    carb2v7 = fields.Float("滲碳層2值7")
    carb2v8 = fields.Float("滲碳層2值8")

    sskv = fields.Float("斷面收縮率值")
    sskv1 = fields.Float("斷面收縮率值1")
    sskv2 = fields.Float("斷面收縮率值2")
    sskv3 = fields.Float("斷面收縮率值3")
    sskv4 = fields.Float("斷面收縮率值4")
    sskv5 = fields.Float("斷面收縮率值5")
    sskv6 = fields.Float("斷面收縮率值6")
    sskv7 = fields.Float("斷面收縮率值7")
    sskv8 = fields.Float("斷面收縮率值8")

    safeload = fields.Float("安全負荷值")
    safeload1 = fields.Float("安全負荷值1")
    safeload2 = fields.Float("安全負荷值2")
    safeload3 = fields.Float("安全負荷值3")
    safeload4 = fields.Float("安全負荷值4")
    safeload5 = fields.Float("安全負荷值5")
    safeload6 = fields.Float("安全負荷值6")
    safeload7 = fields.Float("安全負荷值7")
    safeload8 = fields.Float("安全負荷值8")
    HV1 = fields.Integer("HV1")
    HV2 = fields.Integer("HV2")
    HV3 = fields.Integer("HV3")
    HV12 = fields.Integer("HV12")
    HV12OK = fields.Char("HV12OK")
    HV13 = fields.Integer("HV13")
    HV13OK = fields.Char("HV13OK")

    hs5 = fields.Boolean("頭部敲擊5")
    hs10 = fields.Boolean("頭部敲擊10")
    hs15 = fields.Boolean("頭部敲擊15")
    hs7 = fields.Boolean("頭部敲擊7")
    hs30 = fields.Boolean("頭部敲擊30")

    curv5 = fields.Boolean("彎曲度5")
    curv15 = fields.Boolean("彎曲度15")
    curv30 = fields.Boolean("彎曲度30")
    wholeck = fields.Selection([('合格', '合格'), ('不合格', '不合格'), ('待處理', '待處理')], '整體判定')
    faceck = fields.Selection([('合格', '合格'), ('不合格', '不合格')], '外觀判定')
    ck_person = fields.Many2one("yc.hr", string="檢驗人員")
    singleton = fields.Float("單支重")
    uqbuckets = fields.Integer("不合格桶數")
    uqemtreat = fields.Char("不合格特急處理動作")
    produceday1 = fields.Date("製造日期1")
    shift1 = fields.Many2one("yc.setshift", string="班別1")
    op1 = fields.Many2one("yc.hr", string="操作人員1")
    buckets1 = fields.Integer("桶數1")
    teamlead1 = fields.Many2one("yc.hr", string="組長1")
    produceday2 = fields.Date("製造日期2")
    shift2 = fields.Many2one("yc.setshift", string="班別2")
    op2 = fields.Many2one("yc.hr", string="操作人員2")
    buckets2 = fields.Integer("桶數2")
    teamlead2 = fields.Many2one("yc.hr", string="組長2")
    produceday3 = fields.Date("製造日期3")
    shift3 = fields.Many2one("yc.setshift", string="班別3")
    op3 = fields.Many2one("yc.hr", string="操作人員3")
    buckets3 = fields.Integer("桶數3")
    teamlead3 = fields.Many2one("yc.hr", string="組長3")
    weighbuckets = fields.Integer("磅後桶數")
    bdiff = fields.Integer("桶數差")
    pweight = fields.Integer("進貨重量")
    tweight = fields.Integer("磅後總重")
    wdiff = fields.Integer("重量差")
    currnt_furno = fields.Char("現在爐號")
    serial = fields.Float("序號", default=99.9)
    giveday = fields.Char("應對交期")
    ptime1 = fields.Char("製造時間1")
    ptime2 = fields.Char("製造時間2")
    ptime3 = fields.Char("製造時間3")
    p_op = fields.Many2one("yc.hr", string="產量操作人員")
    p_weight = fields.Many2one("yc.hr", string="產量過磅人員")
    pnote = fields.Char("產量備註")
    ckresist = fields.Boolean("CK抗拉強度")
    cksurfhrd = fields.Boolean("CK表面硬度")
    ckcorehrd = fields.Boolean("CK心部硬度")
    ckcl = fields.Boolean("CK滲碳層")
    cksfhv = fields.Boolean("CK表面硬度值")
    ckchv = fields.Boolean("CK心部硬度值")
    ckrtens = fields.Boolean("CK抗拉強度值")
    ckyv = fields.Boolean("CK降伏強度值")
    ckelong = fields.Boolean("CK伸長率值")
    cktv = fields.Boolean("CK扭力強度值")
    ckcl1v = fields.Boolean("CK滲碳層1值")
    cksskv = fields.Boolean("CK斷面收縮率值")
    cksl = fields.Boolean("CK安全負荷值")
    ckysvste = fields.Boolean("CK降伏點值起迄")
    ckmlste = fields.Boolean("CK最大負荷值起迄")
    cksskste = fields.Boolean("CK斷面積值起迄")
    qcnote = fields.Many2one("yc.setqcnote", string="品管備註")
    pw1 = fields.Integer("製造重量1")
    pw2 = fields.Integer("製造重量2")
    pw3 = fields.Integer("製造重量3")
    ckecl = fields.Boolean("CK脫碳層")
    ckecl2v = fields.Boolean("CK滲碳層2值")
    ckwhrd = fields.Boolean("CK華司硬度")
    ckhf = fields.Many2one("yc.sethardness", string="華司硬度規格")
    ffday = fields.Date("完爐日期")
    fftime = fields.Char("完爐時間")
    ckclv = fields.Boolean("CK滲碳層")
    feedbucket = fields.Integer("入料桶數")
    feedweight = fields.Integer("入料總重")
    productname = fields.Many2one("yc.setproduct", string="產品名稱")
    contrast = fields.Float("對照")
    shipbucket = fields.Integer("出貨桶數")
    shipweight = fields.Integer("出貨重量")
    sskvste = fields.Char("斷面收縮率值起迄")
    slste = fields.Char("安全負荷值起迄")
    ckhs = fields.Boolean("CK頭部敲擊")
    ckcurv = fields.Boolean("CK彎曲度")
    ckmxl = fields.Boolean("CK最大負荷")
    mxload = fields.Char("最大負荷")
    cktorsion = fields.Boolean("CK扭力強度")
    tlevel = fields.Float("扭力強度")
    ckwhrd1v = fields.Boolean("CK華司硬度1值")
    ckwhrd2v = fields.Boolean("CK華司硬度2值")
    whrd2v1 = fields.Float("華司硬度2值1")
    whrd2v2 = fields.Float("華司硬度2值2")
    whrd2v3 = fields.Float("華司硬度2值3")
    whrd2v4 = fields.Float("華司硬度2值4")
    whrd2v5 = fields.Float("華司硬度2值5")
    whrd2v6 = fields.Float("華司硬度2值6")
    whrd2v7 = fields.Float("華司硬度2值7")
    whrd2v8 = fields.Float("華司硬度2值8")
    uqtreat = fields.Char("不合格品處理")
    uqweight = fields.Integer("不合格重量")
    followup = fields.Char("處理方式")
    # should be one2many
    clnorm = fields.Char("滲碳層規格")
    statecopy = fields.Char("狀態備份")
    amp1 = fields.Float("圖倍率1")
    amp2 = fields.Float("圖倍率2")
    amp3 = fields.Float("圖倍率3")
    amp4 = fields.Float("圖倍率4")
    amp5 = fields.Float("圖倍率5")
    amp6 = fields.Float("圖倍率6")
    mgreviewday = fields.Date("金相審核日期")
    mgcheckday = fields.Date("金相檢驗日期")
    mgreviewer = fields.Many2one("yc.hr", string="金相審核人員")
    mgchecker = fields.Many2one("yc.hr", string="金相檢驗人員")
    mgrtell = fields.Char("狀態備份")
    mgresult = fields.Char("狀態備份")

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

    @api.model
    def _fetch_create_date(self):
        self.copy_createdate = self.create_date[:10]

    # 1.過濾該天幾張過磅單 並在car_no fields 顯示 該天單號之進貨(I)車次序號
    @api.onchange("day")
    def _filter_car_no(self):
        return {'domain': {"car_no": [("day", "=", self.day), ("in_out", "=", "I")]}}

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

    # 4. 選完車次序號，選擇過磅項目(哪間加工廠)
    @api.depends('processing_attache')
    def _compute_process(self):
        if self.processing_attache:
            for rec in self:
                self.combo_process = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.processing_id.phone, self.processing_attache.processing_id.contact)
                self.combo_customer = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.customer_id.phone, self.processing_attache.customer_id.contact)
                self.customer_id = self.processing_attache.customer_id.id

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
                norm_parameter = rec.env["yc.setnorm"].search([('id', '=', rec.norm_code.id)]).parameter1
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
        self.totalpack = (self.num1 or 0) + (self.num2 or 0) + (self.num3 or 0) + (self.num4 or 0)

    # 邊在輸入進貨資料時，系統就會一邊在幫我們蒐尋舊資料,品名分類、品名、強度級數、材質、規格、加工方式、線材爐號
    # 新增搜尋的form
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

    saveorread = fields.Char("儲存管制作業")

    # # create 管制
    @api.model
    def create(self, vals):
        # 進貨作業 S03N0120
        if self._context.get('params')['action'] == 81:
            # 儲存時給工令號
            cn = vals["car_no"]
            weight_item = self.env['yc.weight']
            weight_cn = weight_item.search([('id', '=', cn)]).carno
            purchase = self.env["yc.purchase"]
            search = purchase.search([("name", "like", weight_cn)])
            number = len(search) + 1
            name = str(weight_cn) + str('%d') % number
            vals.update({"name": name})
        return super(YcPurchase, self).create(vals)

    #
    # @api.model
    # def write(self, vals):
    #     return super(YcPurchase, self).write(vals)

    ckimportdate = fields.Char("進貨距今", compute="_ten_days_check")

    # 分爐排程進貨日期距現在日期超過十天返色提醒
    @api.depends("day", "ckimportdate")
    def _ten_days_check(self):
        if self._context.get('params')['action'] == 109:
            for rec in self:
                if rec.day:
                    rec_day = dt.strptime(rec.day.replace("-", ""), "%Y%m%d").date()
                    elapse = (dt.today().date() - rec_day).days
                    if elapse > 10:
                        rec.ckimportdate = 'over'

    # 在爐內進貨 序號改完要馬上更新資料庫資料
    def update_serial(self):
        vals = {"serial": self.serial}
        purchase = self.env["yc.purchase"].search([("id", "=", self.id)])
        purchase.write(vals)

    # 重排序號(except 99.9 然後轉成未進爐)
    def reorganize(self):
        purchase = self.env["yc.purchase"]
        rows = purchase.search([("order_furn", "=", self.order_furn.id), ("serial", "!=", 99.9)])
        purchase_list = []
        for row in rows:
            purchase_list.append([row.id, row.serial])
        # 重新排序
        purchase_list = sorted(purchase_list, key=lambda s: s[1])
        # 重新賦值
        for x in range(len(rows)):
            purchase_list[x][1] = x + 1
        # update data
        for row in purchase_list:
            purchase.search([("id", "=", row[0])]).write({'serial': row[1], 'status': 4})
        # 99.9 狀態轉未進爐
        notin_list = purchase.search([("order_furn", "=", self.order_furn.id), ("serial", "=", 99.9)])
        for row in notin_list:
            notin_list.search([("id", "=", row.id)]).write({'status': 4})

    # S05N0100 製程登錄作業
    # 以下為查詢欄位
    searchname = fields.Char("工令查詢")
    furn_in = fields.Many2one("yc.purchase", string="已進爐")
    furn_notin = fields.Many2one("yc.purchase", string="未進爐")

    @api.onchange("searchname")
    def yc_purchase_search_name(self):
        # 如果是在製程登錄作業的form 查詢工令時將進行跳轉
        if self._context.get('params')['action'] == 111:
            # S05N0100 製程登錄作業
            purchase = self.env["yc.purchase"]
            to_delete_id = purchase.search([('name', '=', self.searchname)], order='id desc', limit=1).id
            # 把odoo 自動儲存的複製record 或 ODOO產生的空資料刪除
            sql = "delete from yc_purchase where id=%d or name is NULL" % to_delete_id
            repeated_name_record = self.env["yc.purchase"].search([('name', '=', self.searchname)])
            empty_name_record = self.env["yc.purchase"].search([('name', '=', None)])
            if len(repeated_name_record) > 1 or len(empty_name_record) >= 1:
                self._cr.execute(sql)
            id = self.env['yc.purchase'].search(
                [('name', '=', self.searchname or self.furn_in.name or self.furn_notin.name)]).id
            # purchase = self.env['yc.purchase'].search([('name', '=', self.searchname)])
            # self.saveorread = "read"
            # # self.id = purchase.id
            # self.name = purchase.name
            # self.day = purchase.day
            # self.wire_furn = purchase.wire_furn
            return {
                'name': self.searchname,
                'res_model': 'yc.purchase',
                'type': 'ir.actions.act_window',
                'res_id': id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('yc_root.process_data_entry_form').id,
                'target': 'inline', }

            # 下面是另一種方法去取得record data
            # 但是onchange 也無法觸發下面這段，要用js寫了
            # 'name': 'Go to website',
            # 'res_model': 'ir.actions.act_url',
            # 'type': 'ir.actions.act_url',
            # 'target': 'inline',
            # 'url': 'web?debug#id=%s&view_type=form&model=yc.purchase&menu_id=275&action=111' % id,
            # }

        elif self._context.get('params')['action'] == 112:
            # S05N0200
            to_delete_id = self.env["yc.purchase"].search([('name', '=', self.searchname)], order='id desc', limit=1).id
            sql = "delete from yc_purchase where id=%d" % to_delete_id
            if len(self.env["yc.purchase"].search([('name', '=', self.searchname)])) > 1:
                self._cr.execute(sql)
            id = self.env['yc.purchase'].search([('name', '=', self.searchname)]).id
            return {
                'name': self.searchname,
                'res_model': 'yc.purchase',
                'type': 'ir.actions.act_window',
                'res_id': id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('yc_root.quantity_data_entry_form').id,
                'target': 'inline',
            }
        elif self._context.get('params')['action'] == 124:
            # S04N0200
            to_delete_id = self.env["yc.purchase"].search([('name', '=', self.searchname)], order='id desc', limit=1).id
            sql = "delete from yc_purchase where id=%d" % to_delete_id
            if len(self.env["yc.purchase"].search([('name', '=', self.searchname)])) > 1:
                self._cr.execute(sql)
            id = self.env['yc.purchase'].search([('name', '=', self.searchname)]).id
            return {
                'name': self.searchname,
                'res_model': 'yc.purchase',
                'type': 'ir.actions.act_window',
                'res_id': id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('yc_root.quality_form').id,
                'target': 'inline',
            }

    # 各查詢表單後更新資料
    def save_process_data(self):
        self.saveorread = "save"
        return True

    # S05N0200 製程登錄作業
    weighted_order = fields.Many2one("yc.purchase", string="已過磅")
    notweighted_order = fields.Many2one("yc.purchase", string="未過磅")
    produce_details_ids = fields.One2many("yc.produce.details", "name", "製造明細")
    count = fields.Integer("數桶數", default=1)

    # 過濾桶號工令
    @api.onchange("order_furn")
    def _chech_order(self):
        if self._context.get('params')['action'] == 111:
            return {"domain": {"furn_in": [("order_furn", "=", self.order_furn.id), ("status", "=", 6)],
                               "furn_notin": [("order_furn", "=", self.order_furn.id), ("status", "=", 4)]}}
        elif self._context.get('params')['action'] == 112:
            return {"domain": {"weighted_order": [("order_furn", "=", self.order_furn.id)],
                               "notweighted_order": [("order_furn", "=", self.order_furn.id)]}}

    # 清除製造條件
    def clear_produce_data(self):
        to_clear_field = ['produceday1', 'ptime1', 'shift1', 'op1', 'buckets1', 'pw1', 'teamlead1',
                          'produceday2', 'ptime2', 'shift2', 'op2', 'buckets2', 'pw2', 'teamlead2',
                          'produceday3', 'ptime3', 'shift3', 'op3', 'buckets3', 'pw3', 'teamlead3',
                          'ffday', 'fftime', 'flow', 'cp', 'nh31', 'nh32', 'nh33', 'nh34', 'heat1',
                          'heat2', 'heat3', 'heat4', 'heat5', 'heat6', 'heat7', 'heat8', 'heattemp',
                          'heatsped', 'pre_furn', 'tempturing1', 'tempturing2', 'tempturing3', 'tempturing4',
                          'tempturing5', 'tempturing6', 'tempturisped', 'currnt_furno', 'notices1', 'notices2',
                          'notices3', 'qcnote1', 'qcnote2', 'qcnote3', 'prodnote1', 'prodnote2', 'prodnote3']
        db = self.env['yc.purchase']
        to_clear_id = db.search([('name', '=', self.name)]).id
        for field in to_clear_field:
            db.search([('id','=',to_clear_id)]).write({field: None})

    # S04N0200 品質數據主檔
    checked = fields.Many2one("yc.purchase", string="已檢驗")
    notchecked = fields.Many2one("yc.purchase", string="未檢驗")

    # 查詢
    # SELECT t1.表面硬度 as 表面硬度值,t1.表面規格 as 表面硬度規格,t1.心部硬度 as 心部硬度值,t1.心部規格 as 心部硬度規格"
    #       ,t1.抗拉強度 as 抗拉強度值,t1.降伏點強度 as 降伏強度值,t1.伸長率 as 伸長率值,t1.滲碳層 as 滲碳層1值 "
    #       ,t1.斷面收縮 as 斷面收縮率值,t1.安全負荷 as 安全負荷值"
    #       ,m.扭力 as 扭力強度值,m.依據標準 as 國際標準 "
    #       FROM 進貨單主檔 m "
    #       LEFT JOIN 產品機械性質主檔 AS t1 ON m.依據標準 = t1.依據標準"
    #       WHERE m.工令號碼 = '" & strKey1 & "'

    # 帶出工令後 找出數據登錄資料
    @api.onchange("searchname")
    def _quality_main_data(self):
        if self._context.get('params')['action'] == 124:
            t1 = self.env["yc.mechanicalproperty"].search([("standard", "=", self.standard)])
            self.sfhv = t1.surfhrd
            self.sfhn = t1.surfaceform
            self.chv = t1.corehrd
            self.chn = t1.coreform
            self.rtens = t1.tensihrd
            self.ysv = t1.ystrength
            self.elohv = t1.elongation
            self.carb1v = t1.carburlayer
            self.sskvste = t1.sectionshrink
            self.safeload = t1.safeload


class YcProduceDetails(models.Model):
    _name = "yc.produce.details"

    name = fields.Many2one("yc.purchase", "工令號碼", ondelete='cascade')
    serail = fields.Integer("序號")
    bucket_no = fields.Integer("桶號")
    emptybucket = fields.Integer("空桶重")
    unit = fields.Many2one("yc.setunit", string="單位")
    rawweight = fields.Integer("生料重")
    rawnetweight = fields.Integer("生料淨重")
    feed_man = fields.Many2one("yc.hr", string="入料人員")
    tweight = fields.Integer("磅後重")
    recevieemptybucket = fields.Integer("收料空桶重")
    recevietunit = fields.Many2one("yc.setunit", string="收料單位")
    tnetweight = fields.Integer("磅後淨重")
    recevie_man = fields.Many2one("yc.hr", string="收料人員")
    weightdiff = fields.Integer("重量差")
    # status = fields.Char("狀態")
    note = fields.Text("備註")

    @api.multi
    @api.onchange("bucket_no")
    def _get_row_number(self):
        # condition1 新增: details檔 無關連record count不用檢查
        # condition2 修改: details檔 有關連record 可以重置count

        p = self.env['yc.purchase']
        self.bucket_no = p.search([('name', '=', self.name.name)]).count
        sql = "UPDATE yc_purchase SET count =%s WHERE name='%s'" % (str(self.bucket_no + 1), self.name.name)
        p._cr.execute(sql)

    @api.onchange("rawweight", "emptybucket", "tweight")
    def _get_rawnetweight(self):
        self.rawnetweight = self.rawweight - self.emptybucket
        self.tnetweight = self.tweight - self.emptybucket
        self.weightdiff = self.rawweight - self.tweight


class YcPurchaseStore(models.Model):
    _name = "yc.purchasestore"

    name = fields.Char("進貨庫存單號")


class YcPurchaseStore(models.Model):
    _name = "yc.purchasereport"

    name = fields.Char("客戶進貨統計表")

# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime as dt
import pytz, logging, collections, re


class YcPurchase(models.Model):
    _name = "yc.purchase"
    _order = 'day desc,time desc'

    name = fields.Char("工令號碼")
    day = fields.Date("進貨日期", default=lambda self: self._default_date())
    time = fields.Char("時間", default=lambda self: self._get_time())
    copy_createdate = fields.Char("製表日期", compute="_fetch_create_date")
    status = fields.Many2one("yc.setstatus", string="狀態",
                             default=lambda self: self.env['yc.setstatus'].search([('name', '=', '未排程')]))
    weighstate = fields.Char("過磅狀態", default="未過磅")
    checkstate = fields.Char("檢驗狀態")
    driver_id = fields.Many2one("yc.driver", string="司機名稱", related="car_no.driver_id")
    factory_id = fields.Many2one("yc.factory", string="所屬工廠", default=lambda self: self.env.user.factory_id)
    company_id = fields.Many2one("res.company", string='所屬工廠', default=lambda self: self.env.user.company_id)
    processing_attache = fields.Many2one("yc.weight.details", "加工廠名稱")
    processing_phone = fields.Char("加工廠電話")
    processing_contact = fields.Char("負責人")

    pre_order = fields.Char("前工令號碼")
    car_no = fields.Many2one("yc.weight", string="車次序號")
    customer_id = fields.Many2one("yc.customer", "客戶名稱", related="processing_attache.customer_id")
    # customer_phone = fields.Char("客戶電話")
    # customer_contact = fields.Char("客戶聯絡人")

    batch = fields.Char("客戶批號")
    customer_no = fields.Char("客戶單號")
    person = fields.Many2one("res.users", string="開單人員")
    list_man = fields.Many2one("res.users", string="開單人員", default=lambda self: self.env.user.id)
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    # 和上面重複
    # productname = fields.Many2one("yc.setproduct", string="產品名稱")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    len_code = fields.Many2one("yc.setlength", string="長度")
    len_descript = fields.Char("長度說明")

    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    surface_code = fields.Many2one("yc.setsurface", string="表面處理")
    elecplswitch = fields.Char("表面處理開關", compute="_switcher", help="當表面處理選定'電鍍'時，turn on，否則off")
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
    storeplace_id = fields.Many2one("yc.setstoreplace", related="processing_attache.storeplace_id")
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
    # 可考慮用autocomplete 就可改用Char
    order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
    currnt_furno = fields.Many2one("yc.setfurnace", string="現在爐號")
    # 好像都沒用到?
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
    op = fields.Many2one("res.users", string="操作人員")
    qc = fields.Many2one("res.users", string="品管人員")
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
    ck_person = fields.Many2one("res.users", string="檢驗人員")
    singleton = fields.Float("單支重")

    uqemtreat = fields.Char("不合格特急處理動作")
    produceday1 = fields.Date("製造日期1")
    shift1 = fields.Many2one("yc.setshift", string="班別1")
    op1 = fields.Many2one("res.users", string="操作人員1")
    buckets1 = fields.Integer("桶數1")
    teamlead1 = fields.Many2one("res.users", string="組長1")
    produceday2 = fields.Date("製造日期2")
    shift2 = fields.Many2one("yc.setshift", string="班別2")
    op2 = fields.Many2one("res.users", string="操作人員2")
    buckets2 = fields.Integer("桶數2")
    teamlead2 = fields.Many2one("res.users", string="組長2")
    produceday3 = fields.Date("製造日期3")
    shift3 = fields.Many2one("yc.setshift", string="班別3")
    op3 = fields.Many2one("res.users", string="操作人員3")
    buckets3 = fields.Integer("桶數3")
    teamlead3 = fields.Many2one("res.users", string="組長3")
    # TODO: 應該是order_wizard才用的到 可考慮刪除
    serial = fields.Float("序號", default=99.9)
    giveday = fields.Char("應對交期")
    ptime1 = fields.Char("製造時間1")
    ptime2 = fields.Char("製造時間2")
    ptime3 = fields.Char("製造時間3")
    p_op = fields.Many2one("res.users", string="產量操作人員")
    p_weight = fields.Many2one("res.users", string="產量過磅人員")
    pnote = fields.Char("產量備註")
    condition = fields.Selection([('IT', '廠內退回'), ('OT', '廠外退回')], string="退回來源")

    # 再列印模式中確認是否要印出
    # TODO: 可以再列印中開的一個wizard, 把check 放在該model，可減少進貨主檔資料
    #  計: 33個
    ck1 = fields.Boolean("品名check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck2 = fields.Boolean("規格check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck3 = fields.Boolean("長度check", default=False, help="在搜尋舊檔wizard自動代入篩選")
    ck4 = fields.Boolean("品名分類check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck5 = fields.Boolean("加工方式check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck6 = fields.Boolean("材質check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck7 = fields.Boolean("強度級數check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    ck8 = fields.Boolean("線材爐號check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    # 以上如果確認用purchase2 這個template 就可以刪掉
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
    ckclv = fields.Boolean("CK滲碳層")
    ckecl = fields.Boolean("CK脫碳層")
    ckecl2v = fields.Boolean("CK滲碳層2值")
    ckwhrd = fields.Boolean("CK華司硬度")
    ckhs = fields.Boolean("CK頭部敲擊")
    ckcurv = fields.Boolean("CK彎曲度")
    ckmxl = fields.Boolean("CK最大負荷")
    cktorsion = fields.Boolean("CK扭力強度")
    ckwhrd1v = fields.Boolean("CK華司硬度1值")
    ckwhrd2v = fields.Boolean("CK華司硬度2值")


    qcnote = fields.Many2one("yc.setqcnote", string="品管備註")
    pw1 = fields.Integer("製造重量1")
    pw2 = fields.Integer("製造重量2")
    pw3 = fields.Integer("製造重量3")
    ckhf = fields.Many2one("yc.sethardness", string="華司硬度規格")
    ffday = fields.Date("完爐日期")
    fftime = fields.Char("完爐時間")
    contrast = fields.Float("對照")
    shipbucket = fields.Integer("出貨桶數")
    shipweight = fields.Integer("出貨重量")
    sskvste = fields.Char("斷面收縮率值起迄")
    slste = fields.Char("安全負荷值起迄")
    mxload = fields.Char("最大負荷")
    tlevel = fields.Float("扭力強度")
    whrd2v1 = fields.Float("華司硬度2值1")
    whrd2v2 = fields.Float("華司硬度2值2")
    whrd2v3 = fields.Float("華司硬度2值3")
    whrd2v4 = fields.Float("華司硬度2值4")
    whrd2v5 = fields.Float("華司硬度2值5")
    whrd2v6 = fields.Float("華司硬度2值6")
    whrd2v7 = fields.Float("華司硬度2值7")
    whrd2v8 = fields.Float("華司硬度2值8")
    uqtreat = fields.Selection([('f0', '重回火或重染黑'), ('f1', '重做'),
                                ('f2', '報廢'), ('f3', '無'), ('f4', '部分出貨，部分重回火、重染黑、重做')], '不合格品處理')

    pweight = fields.Integer("進貨重量")
    tweight = fields.Integer("磅後總重")
    feedbucket = fields.Integer("入料桶數")
    feedweight = fields.Integer("入料總重")
    weighbuckets = fields.Integer("磅後桶數")
    bdiff = fields.Integer("桶數差")
    wdiff = fields.Integer("重量差")
    uqweight = fields.Integer("不合格重量")
    uqbuckets = fields.Integer("不合格桶數")
    followup = fields.Selection([("migrate", "轉入進貨單"), ("stay", "不轉入進貨單")], "處理方式")

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
    mgreviewer = fields.Many2one("res.users", string="金相審核人員")
    mgchecker = fields.Many2one("res.users", string="金相檢驗人員")
    mgrtell = fields.Char("狀態備份")
    mgresult = fields.Char("狀態備份")


    # 製造明細檔
    produce_details_ids = fields.One2many("yc.produce.details", "name", "製造明細")

    # functional group: 功能性欄位，無須從舊資料匯入
    wizard_check = fields.Boolean("是否帶出", default=False, help='purchase_wizard中，checkbox TorF判斷要帶出哪幾筆資料')
    ckimportdate = fields.Char("進貨距今", compute="_ten_days_check", help="判斷進貨時間是否超過十天，是則返色提醒")
    return_in_fac_check = fields.Boolean(default=False, help="確認要帶出哪筆廠內退回紀錄, refer template: purchase2")
    return_btn = fields.Boolean(default=False, help="觸發display")
    wizard_btn = fields.Boolean(default=False, help="判斷要帶出哪筆")
    # action_id_main = fields.Integer(
    #     default=lambda self: self.env['ir.actions.act_window'].search([('name', '=', '進貨單作業')], limit=1).id,
    #     help="找出資料庫視窗動作ID，搜尋name值\n進貨單作業: 進貨單作業")
    product_code_searchbox = fields.Char("搜尋品名編號")

    # ['searchname','furn_in','furn_notin','weighted_order','notweighted_order','checked', 'notchecked','count' ]
    # searchname = fields.Char("工令查詢", help="搜尋工令欄位")
    # furn_in = fields.Many2one("yc.purchase", string="已進爐")
    # furn_notin = fields.Many2one("yc.purchase", string="未進爐")
    # weighted_order = fields.Many2one("yc.purchase", string="已過磅")
    # notweighted_order = fields.Many2one("yc.purchase", string="未過磅")
    # checked = fields.Many2one("yc.purchase", string="已檢驗")
    # notchecked = fields.Many2one("yc.purchase", string="未檢驗")
    # count = fields.Integer("數桶數", default=1)

    # ['itself_ids','return_in_fac_ids','return_ids','combo_customer','combine_abbrev','combo_process','remainder']
    # display group: 在頁面上展示紀錄，無須從舊資料匯入
    itself_ids = fields.Many2many(comodel_name="yc.purchase", relation='yc_purchase_yc_purchase_rel3',
                                  column1='col_name', column2='col_name_2')
    return_in_fac_ids = fields.Many2many(comodel_name="yc.purchase", relation='yc_purchase_yc_purchase_rel4',
                                         column1='col_name_3', column2='col_name_4')
    return_ids = fields.Many2many("yc.return", string="purchase search", help="廠外退回查詢")
    combo_customer = fields.Char("客戶聯絡資訊", compute='_compute_process')
    combine_abbrev = fields.Char('客戶', compute='_combine')
    combo_process = fields.Char("加工廠聯絡資訊", compute='_compute_process')
    remainder = fields.Char(help="爐內進貨 明細頁提示欄")

    # 加工廠簡稱-客戶簡稱
    @api.depends('processing_attache')
    def _combine(self):
        for rec in self:
            if rec.processing_attache:
                _c = rec.processing_attache.customer_id.abbrev
                _p = rec.processing_attache.processing_id.name
                rec.combine_abbrev = _p + '-' + _c

    @api.onchange('condition')
    def search_purchase(self):
        if self.condition:
            # 處理方式('followup')為 "轉入進貨單"('migrate')者現身
            domain = [('followup', '=', 'migrate')]
            if self.condition == 'OT': #廠外退回
                records = self.env['yc.return'].search(domain)
                self.return_ids = [(6, _, records.ids)]
            elif self.condition == 'IT': #廠內退回
                #  "SELECT 工令號碼 as 出貨退回編號,工令號碼,不合格品處理 as 退回備註,b.前工令號碼"
                #   from 進貨單主檔 a"
                #   left join (select 前工令號碼 from 進貨單主檔) b on a.工令號碼=b.前工令號碼"
                #   WHERE 處理方式='轉入進貨單' and b.前工令號碼 is null"
                #   order by 工令號碼 ASC"
                purchase = self.env['yc.purchase'].search(domain)
                self.return_in_fac_ids = [(6, _, purchase.ids)]

    def comfirm_return(self):
        '''
        1. 確認退回來源
        2. 確認勾選紀錄有幾筆，超過1筆警告
        3. 解掉勾勾
        4. 1筆，找到該紀錄拉出資料
        :return:
        '''
        if self.condition == 'OT':
            checked = self.return_ids.filtered(lambda r: r.wizard_check)
            if len(checked) > 1:
                raise ValidationError(_('只能選一筆'))
            elif len(checked) == 0:
                return 1
            purchase = self.env['yc.purchase']
            # TODO: 待確認 'norcls'(規範分類) 這個從頭到尾沒看過哪一個地方 key-in
            wanted = ['len_code', 'product_code', 'piece', 'customer_no', 'batch', 'len_descript',
                      'norm_code', 'strength_level', 'norcls', 'clsf_code', 'proces_code', 'txtur_code',
                      'surface_code', 'elecpl_code', 'process1', 'process2', 'num1', 'unit1', 'num2',
                      'unit2', 'num3', 'unit3', 'num4', 'unit4', 'order_furn', 'totalpack', 'net',
                      'wire_furn', 'standard', 'surfhrd', 'corehrd', 'tensihrd', 'carburlayer', 'torsion',
                      'wxr_txtur', 'wxr_txtur', 'storeplace_id', 'tempturing2', 'pre_furn', 'notices1',
                      'notices2', 'notices3', 'notices4', 'qcnote1', 'qcnote2', 'qcnote3', 'prodnote1',
                      'prodnote2', 'prodnote3', 'flow', 'cp', 'nh31', 'nh32', 'nh33', 'nh34', 'heat1',
                      'heat2', 'heat3', 'heat4', 'heat5', 'heat6', 'heat7', 'heat8', 'heattemp', 'heatsped',
                      'tempturing1', 'tempturing2', 'tempturing3', 'tempturing4', 'tempturing5',
                      'tempturing6', 'tempturisped', 'fullorhalf'
                      ]
            checked.write({'wizard_check': False})
            record = purchase.search([('name', '=', checked.name)])
            for _field in wanted:
                _val = getattr(record, _field)
                setattr(self, _field, _val)
            # 按下拉出退回btn 會先create() 再經過這裡 所以可以一律用write
            # 生成新的單號 並更新 退回主檔 資料
            _id = purchase.search([('name', '=', self.name)]).id
            checked.write({"neworder": _id})
        elif self.condition == 'IT':
            checked = self.return_in_fac_ids.filtered(lambda r: r.return_in_fac_check)
            if len(checked) > 1:
                raise ValidationError(_('只能選一筆'))
            elif len(checked) == 0:
                return 1
            checked.write({'return_in_fac_check': False})


    #########################
    ### views共用或部分共用 ###
    #########################

    # 1.修正時間
    @api.model
    def _get_time(self):
        user_tz = self.env.user.tz
        now = dt.now(pytz.timezone(user_tz)).strftime("%Y%m%d%H%M%S")
        time = '%s:%s:%s' % (now[8:10], now[10:12], now[12:14])
        return time

    # 2.製表日期
    def _fetch_create_date(self):
        self.copy_createdate = self.create_date[:10]

    # 3.裝袋合計合計處理
    @api.onchange("num1", "num2", "num3", "num4")
    def _count_bag(self):
        self.totalpack = (self.num1 or 0) + (self.num2 or 0) + (self.num3 or 0) + (self.num4 or 0)


    # 4. 工令查詢 之後把這段移到wizard應不用再去刪除空資料
    # TODO: 確定不用後可以刪掉了
    def yc_purchase_search_name(self):
        # 如果是在製程登錄作業的form 查詢工令時將進行跳轉
        if self._context.get('params')['action'] == 111:
            # S05N0100 製程登錄作業
            purchase = self.env["yc.purchase"]
            repeated_name_record = purchase.search(
                [('name', '=', self.searchname), ('company_id', '=', self.env.user.company_id.id)])
            empty_name_record = purchase.search([('name', '=', None), ('company_id', '=', self.env.user.company_id.id)])
            # 把odoo 自動儲存的複製record 或 ODOO產生的空資料刪除
            if len(repeated_name_record) > 1:
                to_delete_id = purchase.search(
                    [('name', '=', self.searchname), ('company_id', '=', self.env.user.company_id.id)], order='id desc',
                    limit=1).id
                sql = "delete from yc_purchase where id=%d" % to_delete_id
                self._cr.execute(sql)
            if len(empty_name_record) >= 1:
                sql = "delete from yc_purchase where name is NULL"
                self._cr.execute(sql)
            id = self.env['yc.purchase'].search(
                [('name', '=', self.searchname or self.furn_in.name or self.furn_notin.name)]).id
            to_create_order = purchase.search([('id', '=', id)])
            if len(to_create_order.produce_details_ids) == 0:
                for i in range(1, 7):
                    to_create_order.produce_details_ids = [(0, 0, {'name': id, 'bucket_no': i})]
            return {
                'name': self.searchname,
                'res_model': 'yc.purchase',
                'type': 'ir.actions.act_window',
                'res_id': id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('yc_root.process_data_entry_form').id,
                'target': 'inline', }
        elif self._context.get('params')['action'] == 124:
            # S04N0200
            to_delete_id = self.env["yc.purchase"].search(
                [('name', '=', self.searchname), ('company_id', '=', self.env.user.company_id.id)], order='id desc',
                limit=1).id
            sql = "delete from yc_purchase where id=%d" % to_delete_id
            if len(self.env["yc.purchase"].search(
                    [('name', '=', self.searchname), ('company_id', '=', self.env.user.company_id.id)])) > 1:
                self._cr.execute(sql)
            id = self.env['yc.purchase'].search(
                [('name', '=', self.searchname), ('company_id', '=', self.env.user.company_id.id)]).id
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


    # 5.各查詢表單後更新資料
    def save_entry_data(self):
        return True

    # 6.過濾桶號工令 (改wizard 應該用不到了)
    @api.onchange("order_furn")
    def _chech_order(self):
        # TODO: should modified value by given number directly.
        if self._context.get('params')['action'] == 111:
            return {"domain": {"furn_in": [("order_furn", "=", self.order_furn.id), ("status", "=", 6)],
                               "furn_notin": [("order_furn", "=", self.order_furn.id), ("status", "=", 4)]}}
        elif self._context.get('params')['action'] == 112:
            return {"domain": {"weighted_order": [("order_furn", "=", self.order_furn.id)],
                               "notweighted_order": [("order_furn", "=", self.order_furn.id)]}}

    # 7.濾出只有和使用者同樣廠別的紀錄
    # 目前以修改odoo11.0 > odoo > http.py L# 1095 讓頁面抓到context 取代這一段功能
    # @api.model
    # def company_filter_filter(self):
    #     ctx = self.env.context.copy()
    #     company_code = self.env.user.company_id.id
    #     # 不知道為什麼上面這段沒作用
    #     ctx.update({'company_id': [company_code]})
    #     if self._context.get('params')['action'] == 81:
    #         reference = self.env.ref('yc_root.purchase_list_action').id
    #     return {
    #         'name': '使用者廠別動態過濾',
    #         'view_type': 'tree',
    #         'view_mode': 'tree,form',
    #         'res_model': 'yc.purchase',
    #         'type': 'ir.actions.act_window',
    #         # 'view_id': reference,
    #         'context': dict(ctx),
    #         'domain': [('company_id', '=', self.env.user.company_id)]
    #     }

    # 8.進貨單wizard 只能帶出一筆資料，超過一筆提醒
    @api.constrains("wizard_check")
    def _check_bringout(self):
        # 出貨作業會拉多筆資料進出貨項目檔，跳過這段提醒
        if self._context.get('params')['action'] != 158:
            wizard_checked = self.env["yc.purchase"].search(
                [('wizard_check', '=', True), ('company_id', '=', self.env.user.company_id.id)])
            if len(wizard_checked) > 1:
                for rec in wizard_checked:
                    rec.write({'wizard_check': False})
                raise Warning("只能選一筆資料帶出")

    # 9. 快速搜尋品名
    @api.onchange('product_code_searchbox')
    def search_box(self):
        if self.product_code_searchbox:
            product = self.env['yc.setproduct']
            domain = [('code', '=', self.product_code_searchbox)]
            # 只能是精準搜尋
            if len(product.search(domain)):
                self.product_code = product.search(domain).id
            else:
                return {'warning': {
                    'title': _('提醒'), 'message': _("沒有這個代碼")}}

    @api.onchange('ck1', 'ck2', 'ck3', 'ck4', 'ck5', 'ck6', 'ck7', 'ck8')
    def _check_out(self):
        if not self.ck1:
            self.product_code = None
        if not self.ck2:
            self.norm_code = None
        if not self.ck3:
            self.len_code = None
        if not self.ck4:
            self.clsf_code = None
        if not self.ck5:
            self.proces_code = None
        if not self.ck6:
            self.txtur_code = None
        if not self.ck7:
            self.strength_level = None
        if not self.ck8:
            self.wire_furn = None
        self._toggle_wizard()

    # 進貨單作業:itself m2m更新、自動帶入參數
    # 爐內進貨  :itself m2m更新
    @api.onchange('product_code', 'clsf_code', 'norm_code', 'proces_code', 'len_code', 'txtur_code',
                  'strength_level', 'wire_furn', 'wizard_btn')
    def _toggle_wizard(self):
        _bool = bool(self.product_code or self.clsf_code or self.norm_code or self.proces_code or
                     self.len_code or self.txtur_code or self.strength_level or self.wire_furn)
        if _bool:
            _action = self.env['ir.actions.act_window']
            action_1 = _action.search([('name', '=', '分爐排程')], limit=1).id
            action_2 = _action.search([('name', '=', '進貨單作業')], limit=1).id
            # itself更新
            purchase = self.env['yc.purchase']
            # 先更新itself

            if self._context['params'].get('action') == action_1 or action_2:
                domain = ()
                if self.product_code and self.ck1:
                    domain += ('product_code', '=', self.product_code.id),
                if self.clsf_code and self.ck4:
                    domain += ('clsf_code', '=', self.clsf_code.id),
                if self.norm_code and self.ck2:
                    domain += ('norm_code', '=', self.norm_code.id),
                if self.proces_code and self.ck5:
                    domain += ('proces_code', '=', self.proces_code.id),
                if self.len_code and self.ck3:
                    domain += ('len_code', '=', self.len_code.id),
                if self.txtur_code and self.ck6:
                    domain += ('txtur_code', '=', self.txtur_code.id),
                if self.strength_level and self.ck7:
                    domain += ('strength_level', '=', self.strength_level.id),
                if self.wire_furn and self.ck8:
                    domain += ('wire_furn', '=', self.wire_furn),
                if len(domain) > 0:
                    # 搜尋出來的list要排除掉自己
                    domain += ('name', '!=', self.name),
                    # 要限制最多六筆 並且時間排序
                    records = purchase.search([d for d in domain], limit=6, order='create_date desc')
                    if len (records) > 0:
                        self.itself_ids = [(6, 0, records.ids)]
                        self.remainder = "共 %s 筆" % len(records)
                    else:
                        self.itself_ids = None
                        self.remainder = "找不到資料"
            # 再看進貨單
            if self._context['params'].get('actions') == action_2:
                domain = ()
                if self.wire_furn:
                    domain += ('wire_furn', '=', self.wire_furn),
                if self.clsf_code:
                    domain += ("clsf_code", "=", self.clsf_code.id),
                if self.product_code:
                    domain += ("product_code", "=", self.product_code.id),
                if self.strength_level:
                    domain += ("strength_level", "=", self.strength_level.id),
                if self.txtur_code:
                    domain += ("txtur_code", "=", self.txtur_code.id),
                if self.norm_code:
                    domain += ("norm_code", "=", self.norm_code.id),
                if self.proces_code:
                    domain += ("proces_code", "=", self.proces_code.id),
                if len(domain) > 0:
                    # 防止搜尋到自己
                    if isinstance(self.id, int):
                        domain += ('id', '!=', self.id),
                    domain += ('company_id', '=', self.env.user.company_id.id),
                    r = purchase.search([d for d in domain], limit=1, order="day desc,time desc")
                    self.flow, self.cp = r.flow, r.cp
                    self.nh31, self.nh32, self.nh33, self.nh34 = r.nh31, r.nh32, r.nh33, r.nh34
                    self.heat1, self.heat2, self.heat3, self.heat4 = r.heat1, r.heat2, r.heat3, r.heat4
                    self.heat5, self.heat6, self.heat7, self.heat8 = r.heat5, r.heat6, r.heat7, r.heat8
                    self.heattemp = r.heattemp
                    self.heatsped = r.heatsped
                    self.tempturing1 = r.tempturing1
                    self.tempturing2 = r.tempturing2
                    self.tempturing3 = r.tempturing3
                    self.tempturing4 = r.tempturing4
                    self.tempturing5 = r.tempturing5
                    self.tempturing6 = r.tempturing6
                    self.tempturisped = r.tempturisped
        else:
            self.itself_ids = None
            self.remainder = "請勾選並依查詢下拉選擇品項"

    # 要拉出itself checked要先寫進資料庫才能判定哪一筆要拉出
    # 用button先進create 再跑這個程式
    def itself_update(self):
        purchase = self.env['yc.purchase']
        checked = purchase.search([('wizard_check', '=', True)])
        for rec in checked:
            rec.write({'wizard_check': False})
        if len(checked) > 1:
            raise ValidationError(_("只能選一筆資料帶出"))
        elif len(checked) == 1:
            _action = self.env['ir.actions.act_window']
            action_1 = _action.search([('name', '=', '分爐排程')], limit=1).id
            action_2 = _action.search([('name', '=', '進貨單作業')], limit=1).id
            # 分爐排程 只拉參數? 還有拉什麼?
            if self._context['params'].get('action') == action_1:
                self.flow = checked.flow
                self.cp = checked.cp
                self.nh31 = checked.nh31
                self.nh32 = checked.nh32
                self.nh33 = checked.nh33
                self.nh34 = checked.nh34
                self.heat1 = checked.heat1
                self.heat2 = checked.heat2
                self.heat3 = checked.heat3
                self.heat4 = checked.heat4
                self.heat5 = checked.heat5
                self.heat6 = checked.heat6
                self.heat7 = checked.heat7
                self.heat8 = checked.heat8
                self.heattemp = checked.heattemp
                self.heatsped = checked.heatsped
                self.tempturing1 = checked.tempturing1
                self.tempturing2 = checked.tempturing2
                self.tempturing3 = checked.tempturing3
                self.tempturing4 = checked.tempturing4
                self.tempturing5 = checked.tempturing5
                self.tempturing6 = checked.tempturing6
                self.tempturisped = checked.tempturisped
            # 進貨作業只拉 設定?
            elif self._context['params'].get('action') == action_2:
                self.surfhrd = checked.surfhrd
                self.corehrd = checked.corehrd
                self.piece = checked.piece
                self.tensihrd = checked.tensihrd
                self.carburlayer = checked.carburlayer
                self.torsion = checked.torsion
                self.tempturing2 = checked.tempturing2
                self.order_furn = checked.order_furn
        self.wizard_btn = False
        # 防止wizard 結束視窗
        return {"type": "set_scrollTop"}

    ######################
    ### purchase.xml用 ###
    ######################
    # 1-1.新增進貨單時過濾過磅單資訊
    @api.onchange("day")
    def _filter_car_no(self):
        return {'domain': {"car_no": [("day", "=", self.day), ("in_out", "=", "I")]}}

    # 1-2.填完車次序號 自動帶出該次司機
    # @api.onchange("car_no")
    # def _driver_id(self):
    #     for rec in self:
    #         rec.driver_id = self.car_no.driver_id.id

    # 1-3.選完車次序號 篩選出該車次之加工廠(找單號)
    @api.onchange("car_no")
    def _filter_processing(self):
        # 這裡 self.car_no.id 是該車次的過磅單號
        return {'domain': {"processing_attache": [("name", "=", self.car_no.id)]}}

    # 1-4. 選完車次序號，選擇過磅項目(哪間加工廠)
    @api.onchange('processing_attache')
    def _compute_process(self):
        if self.processing_attache:
            for rec in self:
                self.combo_process = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.processing_id.phone1 or '', self.processing_attache.processing_id.contact or '')
                self.combo_customer = "電話:  %s    聯絡人:%s" % (
                    self.processing_attache.customer_id.phone1 or '', self.processing_attache.customer_id.contact or '')
                self.customer_id = self.processing_attache.customer_id.id

    # 2.當表面處理開啟'電鍍'時，啟用電鍍類別
    @api.onchange("surface_code")
    def _switcher(self):
        for rec in self:
            elecp = self.env['yc.setelectroplating']
            white = elecp.search([('name', '=', '白皮')])
            ele = elecp.search([('name', '=', '電鍍')])
            black = elecp.search([('name', '=', '黑化')])
            if rec.surface_code.name == '電鍍':
                self.elecplswitch = 'ON'
                self.elecpl_code = ele
            elif rec.surface_code.name == '黑化':
                self.elecpl_code = black
                self.elecplswitch = 'OFF'
            elif rec.surface_code.name == '白皮':
                self.elecpl_code = white
                self.elecplswitch = 'OFF'
            else:
                # 避免非電鍍類別存入資料
                self.elecplswitch = 'OFF'
                rec.elecpl_code = None

    # 3.以品名分類、強度級數、規格，搜尋機械性質主檔並帶出 依據標準、表面硬度、心部硬度、試片、抗拉強度、扭力
    @api.onchange("clsf_code", "strength_level", "norm_code")
    def _fetch_norm_code_info(self):
        if self.norm_code and self.clsf_code and self._context.get('params')['action'] == 81:
            norm = self.env["yc.setnorm"]
            # 規格找出參數值
            norm_para = norm.search([('id', '=', self.norm_code.id)]).parameter1
            machine_property = self.env["yc.mechanicalproperty"]
            torsion = self.env['yc.torsion']
            if self.strength_level:
                strenth_search = ('strength_level', '=', self.strength_level.id)
                mp = machine_property.search([('clsf_code', '=', self.clsf_code.id),
                                              ('stdreviewinit', '<=', float(norm_para)),
                                              ('stdreviewend', '>=', float(norm_para)),
                                              (strenth_search)], limit=1, order="id desc")
                tor = torsion.search([('clsf_code', '=', self.clsf_code.id),
                                      strenth_search,
                                      ("norm_code", "=", self.norm_code.id)], limit=1, order="id desc")
            else:
                mp = machine_property.search([('clsf_code', '=', self.clsf_code.id),
                                              ('stdreviewinit', '<=', float(norm_para)),
                                              ('stdreviewend', '>=', float(norm_para))], limit=1, order="id desc")
                tor = torsion.search([('clsf_code', '=', self.clsf_code.id),
                                      ("norm_code", "=", self.norm_code.id)], limit=1, order="id desc")
            if bool(mp):
                self.standard = mp.standard
                self.surfhrd = mp.innersurfhrd
                self.corehrd = mp.innercorehrd
                self.tensihrd = mp.innertensihrd
                self.carburlayer = mp.innercarburlayer
                self.torsion = tor.torsion1
            else:
                return {
                    'warning': {'title': _('提醒'), 'message': _("沒有這個機械性質")}}

    # 5.進貨單產生工令號
    @api.model
    def create(self, vals):
        _action = self.env['ir.actions.act_window']
        p1 = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context.get('params')['action'] == p1 and vals['car_no']:
            # 儲存時給工令號
            cn = vals["car_no"]
            weight_item = self.env['yc.weight']
            # 如果沒有車次序號要raise error
            weight_cn = weight_item.search([('id', '=', cn)]).carno
            purchase = self.env["yc.purchase"]
            search = purchase.search(
                [("name", "like", weight_cn), ('company_id', '=', self.env.user.company_id.id)])
            number = len(search) + 1
            name = str(weight_cn) + str('%02d') % number
            vals.update({"name": name, 'wizard_btn': False})
        elif self._context.get('params')['action'] == p1 and vals['condition'] == 'IT':
            # TODO: 車次序號用轉廠的車次，待修正
            vals.update({"name": 'TEMP1234', 'wizard_btn': False})
        return super(YcPurchase, self).create(vals)

    # 6.預設時間
    def _default_date(self):
        # 剛載入create 頁面 default不會存值進入field要手動抓action_id
        action = self.env['ir.actions.act_window']
        p1 = action.search([('name', '=', '進貨單作業')]).id
        if self._context.get('params')['action'] == p1:
            return dt.today()

    # 7. 空值警告
    @api.constrains("car_no")
    def _verify(self):
        if not self.car_no and self.condition != "IT":
            raise Warning("車次序號未填")

    # 8. 加熱爐和回火爐自動填值
    @api.onchange('heat2', 'tempturing2')
    def _auto_fill_in(self):
        if self.heat2:
            init = int(self.heat2)
            self.heat1 = init - 30
            self.heat3 = init
            self.heat4 = init
            self.heat5 = init
            self.heat6 = init
            self.heat7 = init
            self.heat8 = init
        if self.tempturing2:
            init = int(self.tempturing2)
            self.tempturing1 = init - 30
            self.tempturing3 = init
            self.tempturing4 = init
            self.tempturing5 = init
            self.tempturing6 = init

    # 8.1 如果其他檢視頁面動到加熱爐2 其他加熱爐需要跟著動
    # Computational fields 不能手動改值
    # @api.depends('tempturing2')
    # def _refer_to_tempt2(self):
    #     init = int(self.tempturing2)
    #     self.tempturing1 = init - 30
    #     self.tempturing3 = init
    #     self.tempturing4 = init
    #     self.tempturing5 = init
    #     self.tempturing6 = init

    ################################
    ### 分爐排程 plan_furna.xml 用 ###
    ################################
    # 1. 分爐排程進貨日期距現在日期超過十天返色提醒
    def _ten_days_check(self):
        if self._context.get('params')['action'] == 187:
            for rec in self:
                if rec.day:
                    rec_day = dt.strptime(rec.day.replace("-", ""), "%Y%m%d").date()
                    elapse = (dt.today().date() - rec_day).days
                    if elapse > 10:
                        rec.ckimportdate = 'over'

    ##################################
    ### 爐類進貨 furna_import.xml 用 ###
    ##################################
    # 1.在爐內進貨 序號改完要馬上更新資料庫資料
    # def update_serial(self):
    #     vals = {"serial": self.serial}
    #     purchase = self.env["yc.purchase"].search(
    #         [("id", "=", self.id), ('factory_id', '=', self.env.user.factory_id.id)])
    #     purchase.write(vals)

    # 2.重排序號(except 99.9 然後轉成未進爐)
    # def reorganize(self):
    #     purchase = self.env["yc.purchase"]
    #     rows = purchase.search([("order_furn", "=", self.order_furn.id), ("serial", "!=", 99.9),
    #                             ('factory_id', '=', self.env.user.factory_id.id)])
    #     purchase_list = []
    #     for row in rows:
    #         purchase_list.append([row.id, row.serial])
    #     # 重新排序
    #     purchase_list = sorted(purchase_list, key=lambda s: s[1])
    #     # 重新賦值
    #     for x in range(len(rows)):
    #         purchase_list[x][1] = x + 1
    #     # update data
    #     for row in purchase_list:
    #         purchase.search([("id", "=", row[0])]).write({'serial': row[1], 'status': 4})
    #     # 99.9 狀態轉未進爐
    #     notin_list = purchase.search([("order_furn", "=", self.order_furn.id), ("serial", "=", 99.9),
    #                                   ('factory_id', '=', self.env.user.factory_id.id)])
    #     for row in notin_list:
    #         notin_list.search([("id", "=", row.id)]).write({'status': 4})

    # 3.爐內進貨導向form view 應該用不到了
    # def review_purchase(self):
    #     return {
    #         'name': self.name,
    #         'res_model': 'yc.purchase',
    #         'type': 'ir.actions.act_window',
    #         'res_id': self.id,
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('yc_root.furna_import_form').id,
    #         'target': 'current',
    #         'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
    #     }

    # 4. 爐內進貨 檢視該紀錄明細(fa-search)
    def action_purchase_display_wizard(self):
        return {
            'name': self.name,
            'res_model': 'yc.purchase',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('yc_root.yc_purchase_display_wizard').id,
            'target': 'new',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
        }

    # 5.
    def wizard_comfirm(self):
        # 修改完更新爐內進貨頁面資料
        purchase = self.env['yc.purchase']
        checked = purchase.search([('wizard_check', '=', True)])
        for to_uncheck in checked:
            to_uncheck.wizard_check = False
        if len(checked) > 1:
            raise ValidationError(_("只能選一筆資料帶出"))
        return

    ###########################
    ######### wizard ##########
    ###########################
    def open_wizard(self):
        return {
            'name': 'test',
            'res_model': 'yc.purchase.wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('yc_root.yc_purchase_wizard').id,
            'target': 'new',
        }

    ###########################
    ### S05N0100 製程登錄作業 ###
    ###########################
    # 1. 登入完轉成已進爐
    @api.multi
    def write(self, vals):
        # 製程登錄作業 S03N0200
        _action = self.env['ir.actions.act_window']
        p1 = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context.get('params')['action'] == p1:
            vals.update({'wizard_btn': False})
        return super(YcPurchase, self).write(vals)

    ###########################
    ### S05N0200 製程登錄作業 ###
    ###########################
    # 1.清除製造條件
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
        to_clear_id = db.search([('name', '=', self.name), ('company_id', '=', self.env.user.company_id.id)]).id
        for field in to_clear_field:
            db.search([('id', '=', to_clear_id)]).write({field: None})

    ###########################
    ### S04N0200 品質數據主檔 ###
    ###########################
    # 查詢
    # SELECT t1.表面硬度 as 表面硬度值,t1.表面規格 as 表面硬度規格,t1.心部硬度 as 心部硬度值,t1.心部規格 as 心部硬度規格"
    #       ,t1.抗拉強度 as 抗拉強度值,t1.降伏點強度 as 降伏強度值,t1.伸長率 as 伸長率值,t1.滲碳層 as 滲碳層1值 "
    #       ,t1.斷面收縮 as 斷面收縮率值,t1.安全負荷 as 安全負荷值"
    #       ,m.扭力 as 扭力強度值,m.依據標準 as 國際標準 "
    #       FROM 進貨單主檔 m "
    #       LEFT JOIN 產品機械性質主檔 AS t1 ON m.依據標準 = t1.依據標準"
    #       WHERE m.工令號碼 = '" & strKey1 & "'

    # 1.帶出工令後 找出數據登錄資料
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

    ### 退回作業搜尋 ###
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = [('name', operator, name)]
        records = self.search(domain + args, limit=limit, order='day desc')
        return records.name_get()


class YcProduceDetails(models.Model):
    # 製造單項目檔
    _name = "yc.produce.details"

    name = fields.Many2one("yc.purchase", "工令號碼", ondelete='cascade')
    serail = fields.Integer("序號")
    bucket_no = fields.Integer("桶號")
    emptybucket = fields.Integer("空桶重")
    unit = fields.Many2one("yc.setunit", string="單位")
    rawweight = fields.Integer("生料重")
    rawnetweight = fields.Integer("生料淨重")
    feed_man = fields.Many2one("res.users", string="入料人員")
    tweight = fields.Integer("磅後重")
    recevieemptybucket = fields.Integer("收料空桶重")
    recevietunit = fields.Many2one("yc.setunit", string="收料單位")
    tnetweight = fields.Integer("磅後淨重")
    recevie_man = fields.Many2one("res.users", string="收料人員")
    weightdiff = fields.Integer("重量差")
    # status = fields.Char("狀態")
    note = fields.Text("備註")

    # @api.multi
    # @api.onchange("bucket_no")
    # def _get_row_number(self):
    #     # condition1 新增: details檔 無關連record count不用檢查
    #     # condition2 修改: details檔 有關連record 可以重置count
    #
    #     p = self.env['yc.purchase']
    #     self.bucket_no = p.search(
    #         [('name', '=', self.name.name), ('company_id', '=', self.env.user.company_id.id)]).count
    #     sql = "UPDATE yc_purchase SET count =%s WHERE name='%s'" % (str(self.bucket_no + 1), self.name.name)
    #     p._cr.execute(sql)

    @api.onchange("rawweight", "emptybucket", "tweight")
    def _get_rawnetweight(self):
        self.rawnetweight = self.rawweight - self.emptybucket
        self.tnetweight = self.tweight - self.emptybucket
        self.weightdiff = self.rawweight - self.tweight

    # 製造項目檔有存入一筆就跳過磅狀態為已過磅
    # @api.model
    # def create(self, vals):
    #     if self._context.get('params')['action'] == 111 and vals['name']:
    #         id = vals['name']
    #         purchase = self.env['yc.purchase'].search(
    #             [('id', '=', id), ('factory_id', '=', self.env.user.factory_id.id)])
    #         if purchase.weighstate == False:
    #             # sql = "update yc_purchase set weighstate='已過磅' where id=%d" % id
    #             # self._cr.execute(sql)
    #             purchase.weighstate = '已過磅'
    #     return super(YcProduceDetails, self).create(vals)

    def write(self, vals):
        if self._context.get('params')['action'] == 188 and self.bucket_no == 1:
            # 找到該工令明細檔的第一桶 磅後重如果大於0 該工令過磅狀態變成已過磅
            if vals['tweight'] > 0:
                vals.update({'weighstate': '已過磅'})
        return super(YcProduceDetails, self).write(vals)


class YcPurchaseStore(models.Model):
    _name = "yc.purchasestore"
    name = fields.Char("進貨庫存單號")


class YcPurchaseStore(models.Model):
    _name = "yc.purchasereport"
    name = fields.Char("客戶進貨統計表")

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import base64, paramiko


class YcQualityWizard(models.TransientModel):
    _name = "yc.quality.wizard"
    searchname = fields.Char("工令查詢", help="搜尋工令欄位")
    name = fields.Char()
    order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
    order_name = fields.Char("工令號碼")
    checked = fields.Many2one("yc.purchase", string="已檢驗")
    notchecked = fields.Many2one("yc.purchase", string="未檢驗")
    invalid = fields.Many2one("yc.purchase", string="不合格")


    day = fields.Date("進貨日期")
    checkstate = fields.Char("檢驗狀態")
    company_id = fields.Many2one("res.company", string='所屬工廠')
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    batch = fields.Char("客戶批號")
    customer_no = fields.Char("客戶單號")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    len_code = fields.Many2one("yc.setlength", string="長度")
    len_descript = fields.Char("長度說明")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    surface_code = fields.Many2one("yc.setsurface", string="表面處理")
    num1 = fields.Integer("數量1")
    unit1 = fields.Many2one("yc.setunit", string="單位代號1")
    num2 = fields.Integer("數量2")
    unit2 = fields.Many2one("yc.setunit", string="單位代號2")
    num3 = fields.Integer("數量3")
    unit3 = fields.Many2one("yc.setunit", string="單位代號3")
    num4 = fields.Integer("數量4")
    unit4 = fields.Many2one("yc.setunit", string="單位代號4")
    net = fields.Integer("淨重")
    standard = fields.Char("依據標準")
    wire_furn = fields.Char("線材爐號")
    headsign = fields.Binary('頭部記號')
    surfhrd = fields.Char("表面硬度")
    corehrd = fields.Char("心部硬度")
    carburlayer = fields.Char("滲碳層")
    torsion = fields.Char("扭力")
    retempt = fields.Integer("回火溫度")
    fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')
    notices1 = fields.Char("注意事項1")
    notices2 = fields.Char("注意事項2")
    notices3 = fields.Char("注意事項3")
    notices4 = fields.Char("注意事項4")
    qcnote1 = fields.Char("品管備註1")
    qcnote2 = fields.Char("品管備註2")
    qcnote3 = fields.Char("品管備註3")
    currnt_furno = fields.Many2one("yc.setfurnace", string="現在爐號")
    pre_furn = fields.Char("以前爐號")
    wxrhard = fields.Char("華司硬度")

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
    produceday = fields.Date("製造日期")
    produceday1 = fields.Date("製造日期1")
    produceday2 = fields.Date("製造日期2")
    produceday3 = fields.Date("製造日期3")
    ptime = fields.Char("製造時間")
    ptime1 = fields.Char("製造時間1")
    ptime2 = fields.Char("製造時間2")
    ptime3 = fields.Char("製造時間3")
    ffday = fields.Date("完爐日期")
    fftime = fields.Char("完爐時間")
    op = fields.Many2one("res.users", string="操作人員")
    op1 = fields.Many2one("res.users", string="操作人員1")
    op2 = fields.Many2one("res.users", string="操作人員2")
    op3 = fields.Many2one("res.users", string="操作人員3")
    shift = fields.Many2one("yc.setshift", string="班別")
    shift1 = fields.Many2one("yc.setshift", string="班別1")
    shift2 = fields.Many2one("yc.setshift", string="班別2")
    shift3 = fields.Many2one("yc.setshift", string="班別3")
    buckets1 = fields.Integer("桶數1")
    buckets2 = fields.Integer("桶數2")
    buckets3 = fields.Integer("桶數3")
    teamlead1 = fields.Many2one("res.users", string="組長1")
    teamlead2 = fields.Many2one("res.users", string="組長2")
    teamlead3 = fields.Many2one("res.users", string="組長3")


    # ck1 = fields.Boolean("品名check", help="在搜尋舊檔wizard自動代入篩選")
    # ck2 = fields.Boolean("規格check", help="在搜尋舊檔wizard自動代入篩選")
    # ck3 = fields.Boolean("長度check", help="在搜尋舊檔wizard自動代入篩選")
    # ck4 = fields.Boolean("品名分類check", help="在搜尋舊檔wizard自動代入篩選")
    # ck5 = fields.Boolean("加工方式check", help="在搜尋舊檔wizard自動代入篩選")
    # ck6 = fields.Boolean("材質check", help="在搜尋舊檔wizard自動代入篩選")
    # ck7 = fields.Boolean("強度級數check", help="在搜尋舊檔wizard自動代入篩選")
    # ck8 = fields.Boolean("線材爐號check", help="在搜尋舊檔wizard自動代入篩選")
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
    ckhf = fields.Many2one("yc.sethardness", string="華司硬度規格")
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
    file = fields.Binary("檔案")


    uqtreat = fields.Selection([('f0', '重回火或重染黑'), ('f1', '重做'),
                                ('f2', '報廢'), ('f3', '無'), ('f4', '部分出貨，部分重回火、重染黑、重做')], '不合格品處理')
    followup = fields.Selection([("migrate", "轉入進貨單"), ("stay", "不轉入進貨單")], "處理方式")
    pweight = fields.Integer("進貨重量")
    tweight = fields.Integer("磅後總重")
    totalpack = fields.Char("裝袋合計")
    feedbucket = fields.Integer("入料桶數")
    feedweight = fields.Integer("入料總重")
    weighbuckets = fields.Integer("磅後桶數")
    bdiff = fields.Integer("桶數差")
    wdiff = fields.Integer("重量差")
    uqweight = fields.Integer("不合格重量")
    uqbuckets = fields.Integer("不合格桶數")
    produce_details_ids = fields.Many2many("yc.produce.details")


    # since <img> attr scr can direct get img from directory, this method cloud be abandoned
    # def _default_image(self):
    #     image_path = modules.get_module_resource('yc_root', 'static/src/img', 'sessional_view.png')
    #     return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))
    #
    # image = fields.Binary('Image', default=_default_image, attachment=True,
    #                       help="background img.")

    def quality_review_search_name(self):
        if bool(self.searchname or self.checked or self.notchecked) == True:
            purchase = self.env["yc.purchase"]
            _name = self.searchname or self.checked.name or self.notchecked.name
            # _company  = self.env.user.company_id.id
            _id = purchase.search([('name', '=', _name)]).id
            if _id:
                self._display_record(_id)
            else:
                raise ValidationError(_('沒有這一筆資料'))

    def _display_record(self, record_id):
        purchase = self.env["yc.purchase"]
        record = purchase.search([('id', '=', record_id)])
        # 蒐集attr_name list
        # getattr() 返回物件屬性值
        # setattr() 設置物件屬性值
        # TODO: 整理進貨主檔，在各資料表那些欄位有需要把資料寫出
        #  oder: yc.purchase > yc.purchase.process > yc.purchase.quantity >
        #        yc.quality.wizard > yc.quality.invalid
        functional_group = ['order_furn', 'notweighted_order', 'weighted_order', 'searchname',
                            'invalid', 'followup', 'invalid_followup', 'checked', 'notchecked',
                            'furn_in', 'furn_notin', 'count', 'produce_details_ids']
        invalid_group = ['pweight', 'tweight', 'totalpack', 'feedbucket', 'feedweight', 'weighbuckets',
                         'bdiff', 'wdiff', 'uqweight', 'uqbucket', 'produce_details_ids', 'uqtreat']

        _action = self.env['ir.actions.act_window']
        Q1 = _action.search([('name', '=', '品質數據主檔_wizard')]).id
        Q2 = _action.search([('name', '=', '不合格品處理作業')]).id
        if self._context['params'].get('action') == Q1:
            for fn in self._proper_fields._map.keys():
                if fn in ['id', 'file'] or fn in invalid_group:
                    pass
                elif fn in ['order_name', 'name']:
                    setattr(self, fn, record.name)
                elif fn in functional_group:
                    setattr(self, fn, None)
                else:
                    _value = getattr(record, fn)
                    setattr(self, fn, _value)
        elif self._context['params'].get('action') == Q2:
            for fn in self._proper_fields._map.keys():
                if fn in ['id', 'file']:
                    pass
                elif fn in ['order_name', 'name']:
                    setattr(self, fn, record.name)
                elif fn in functional_group:
                    setattr(self, fn, None)
                else:
                    _value = getattr(record, fn)
                    setattr(self, fn, _value)

    @api.onchange("order_furn")
    def _chech_order(self):
        return {"domain": {"notchecked": [("order_furn", "=", self.order_furn.id), ("checkstate", "=", False)],
                           "checked": [("order_furn", "=", self.order_furn.id), ("checkstate", "!=", False)],
                           "invalid":[(("order_furn", "=", self.order_furn.id), ("checkstate", "=", "檢驗不合格"))]
                           }}

    def save_quality(self):
        _action = self.env['ir.actions.act_window']
        Q1 = _action.search([('name', '=', '品質數據主檔_wizard')]).id
        Q2 = _action.search([('name', '=', '不合格品處理作業')]).id
        purchase = self.env['yc.purchase']
        domain = [('name', '=', self.name)]
        record = purchase.search(domain)
        if self._context['params'].get('action') == Q1:
            if self.wholeck == '合格' and self.faceck == '合格':
                self.checkstate = '檢驗合格'
            elif self.wholeck == '待處理':
                self.checkstate = '待處理'
            else:
                self.checkstate = '檢驗不合格'
            vals = {}
            for fn in self._proper_fields._map.keys():
                functional_group = ['order_furn', 'notweighted_order', 'weighted_order', 'searchname',
                                    'invalid', 'followup', 'invalid_followup', 'produce_details_ids', 'file']
                _val = getattr(self, fn)
                # TODO: 找出需要更動的欄位再寫入
                if fn not in functional_group:
                    if fn == 'produce_details_ids':
                        pass
                    elif hasattr(_val, 'id'):
                        vals.update({fn: _val.id})
                    else:
                        vals.update({fn: _val})
            record.write({vals})
        elif self._context['params'].get('action') == Q2:
            # TO BE CONTINUE
            pass
        return

    def read_data_in_server(self):
        hostname = '172.31.39.149'
        username = 'admin'
        password = 'admin'
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file('/tmp/sshppk/openssh_yc_root', password='yc_root')
        client.connect(hostname, pkey=key)
        stdin, stdout, stderr = client.exec_command('cat /tmp/yc_data/90106001.50t')
        net_dump = stdout.readlines()
        print(net_dump)

    def call_quality_sample(self):
        if self.order_name:
            purchase = self.env['yc.purchase']
            record = purchase.search([('name', '=', self.order_name)])
            data = {
                'id': self.id,
                'model': self._name,
                'form': {
                    'order_id': record.id,
                },
            }
            # use `module_name.report_id` as reference.
            # `report_action()` will call `get_report_values()` and pass `data` automatically.
            return self.env.ref('yc_root.action_quality_sample').report_action(self, data=data)

    def call_quality_examine_reoort(self):
        if self.order_name:
            purchase = self.env['yc.purchase']
            record = purchase.search([('name', '=', self.order_name)])
            data = {
                'id': self.id,
                'model': self._name,
                'form': {
                    'order_id': record.id,
                },
            }
            # use `module_name.report_id` as reference.
            # `report_action()` will call `get_report_values()` and pass `data` automatically.
            return self.env.ref('yc_root.action_quality_examine_report').report_action(self, data=data)


    def call_quality_unqualified_treatment(self):
        if self.order_name:
            purchase = self.env['yc.purchase']
            record = purchase.search([('name', '=', self.order_name)])
            data = {
                'id': self.id,
                'model': self._name,
                'form': {
                    'order_id': record.id,
                },
            }
            # use `module_name.report_id` as reference.
            # `report_action()` will call `get_report_values()` and pass `data` automatically.
            return self.env.ref('yc_root.action_quality_unqualified_treatment').report_action(self, data=data)

class YcQualityReport(models.AbstractModel):
    '''restrict form "report.module_name.template_id"'''
    _name = 'report.yc_root.report_quality_sample'

    @api.model
    def get_report_values(self, docids, data=None):
        _id = data['form']['order_id']
        purchase = self.env['yc.purchase']
        r = purchase.search([('id', '=', _id)])
        docs = []
        docs.append({
            'customer_id': r.customer_id.abbrev,
            'product_code':r.product_code.name,
            'produceday': r.produceday,
            'norm_code':r.norm_code.name,
            'len_code':r.len_code.name,
            'txtur_code':r.txtur_code.name,
            'wire_furn':r.wire_furn,
            'num1':r.num1,
            'unit1':r.unit1.name,
            'proces_code':r.proces_code.name,
            'surface_code':r.surface_code.name,
            'elecpl_code':r.elecpl_code.name,
            'name':r.name,
            'batch':r.batch,
            'surfhrd':r.surfhrd,
            'corehrd':r.corehrd,
            'carburlayer':r.carburlayer,
            'tensihrd':r.tensihrd,
            'torsion':r.torsion,
            'day':r.day,
            'ck_person':r.ck_person.name,
            'prodnote1': r.prodnote1,
            'prodnote2': r.prodnote2,
            'prodnote3': r.prodnote3,
            'notices1': r.notices1,
            'notices2': r.notices2,
            'notices3': r.notices3,
            'storeplace_id': r.storeplace_id.name,
            'net': r.net,
            'len_descript': r.len_descript,
            'process1': r.process1,
        })
        return {'doc_id': _id,
                'doc_model': 'yc.purchase',
                'docs': docs}

class YcQualityExamineReport(models.AbstractModel):
    '''restrict form "report.module_name.template_id"'''
    _name = 'report.yc_root.report_quality_examine'

    @api.model
    def get_report_values(self, docids, data=None):
        _id = data['form']['order_id']
        # 客戶、品名、製造日期
        # 規格、長度
        # 材質、線材爐
        # 數量1、單位1
        # 加工、表面處理、電鍍別
        # 單號 barcode
        # 客戶批號
        # 表面、心部硬度，滲碳層，拉力，扭力
        # 進貨日期、檢驗員
        purchase = self.env['yc.purchase']
        r = purchase.search([('id', '=', _id)])
        docs = []
        docs.append({
            'customer_id': r.customer_id.abbrev,
            'product_code':r.product_code.name,
            'produceday': r.produceday,
            'norm_code':r.norm_code.name,
            'len_code':r.len_code.name,
            'len_descript': r.len_descript,
            'txtur_code':r.txtur_code.name,
            'wire_furn':r.wire_furn,
            'num1':r.num1,
            'unit1':r.unit1.name,
            'proces_code':r.proces_code.name,
            'surface_code':r.surface_code.name,
            'elecpl_code':r.elecpl_code.name,
            'name':r.name,
            'batch':r.batch,
            'surfhrd':r.surfhrd,
            'corehrd':r.corehrd,
            'carburlayer':r.carburlayer,
            'tensihrd':r.tensihrd,
            'torsion':r.torsion,
            'day':r.day,
            'ck_person':r.ck_person.name,
        })
        return {'doc_id': _id,
                'doc_model': 'yc.purchase',
                'docs': docs}

class YcQualityUnqualifiedTreatment(models.AbstractModel):
    '''restrict form "report.module_name.template_id"'''
    _name = 'report.yc_root.report_quality_unqualified_treatment'

    @api.model
    def get_report_values(self, docids, data=None):
        _id = data['form']['order_id']
        # 客戶、品名、製造日期
        # 規格、長度
        # 材質、線材爐
        # 數量1、單位1
        # 加工、表面處理、電鍍別
        # 單號 barcode
        # 客戶批號
        # 表面、心部硬度，滲碳層，拉力，扭力
        # 進貨日期、檢驗員
        purchase = self.env['yc.purchase']
        r = purchase.search([('id', '=', _id)])
        docs = []
        docs.append({
            'customer_id': r.customer_id.abbrev,
            'product_code':r.product_code.name,
            'produceday': r.produceday,
            'norm_code':r.norm_code.name,
            'len_code':r.len_code.name,
            'len_descript': r.len_descript,
            'txtur_code':r.txtur_code.name,
            'wire_furn':r.wire_furn,
            'num1':r.num1,
            'unit1':r.unit1.name,
            'proces_code':r.proces_code.name,
            'surface_code':r.surface_code.name,
            'elecpl_code':r.elecpl_code.name,
            'name':r.name,
            'batch':r.batch,
            'surfhrd':r.surfhrd,
            'corehrd':r.corehrd,
            'carburlayer':r.carburlayer,
            'tensihrd':r.tensihrd,
            'torsion':r.torsion,
            'day':r.day,
            'ck_person':r.ck_person.name,
        })
        return {'doc_id': _id,
                'doc_model': 'yc.purchase',
                'docs': docs}
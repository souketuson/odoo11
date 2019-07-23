# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class YcPurchaseDisplay(models.TransientModel):
    _name = 'yc.purchase.quantity'

    searchname = fields.Char("工令查詢", help="搜尋工令欄位")

    order_name = fields.Char("工令號碼")
    hidden_name = fields.Char("工令號碼")
    order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
    notweighted_order = fields.Many2one("yc.purchase", string="未過磅")
    weighted_order = fields.Many2one("yc.purchase", string="已過磅")
    day = fields.Date("進貨日期")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    wire_furn = fields.Char("線材爐號")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    batch = fields.Char("客戶批號")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    surface_code = fields.Many2one("yc.setsurface", string="表面處理")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    tensihrd = fields.Char("抗拉強度")
    surfhrd = fields.Char("表面硬度")
    corehrd = fields.Char("心部硬度")
    carburlayer = fields.Char("滲碳層")
    produceday1 = fields.Date("製造日期1")
    ptime1 = fields.Char("製造時間1")
    num1 = fields.Integer("數量1")
    unit1 = fields.Many2one("yc.setunit", string="單位代號1")
    num2 = fields.Integer("數量2")
    unit2 = fields.Many2one("yc.setunit", string="單位代號2")
    num3 = fields.Integer("數量3")
    unit3 = fields.Many2one("yc.setunit", string="單位代號3")
    num4 = fields.Integer("數量4")
    unit4 = fields.Many2one("yc.setunit", string="單位代號4")
    totalpack = fields.Char("裝袋合計")
    pweight = fields.Integer("進貨重量")
    pre_furn = fields.Char("以前爐號")
    feedbucket = fields.Integer("入料桶數")
    feedweight = fields.Integer("入料總重")
    currnt_furno = fields.Many2one("yc.setfurnace", string="現在爐號")
    weighbuckets = fields.Integer("磅後桶數")
    tweight = fields.Integer("磅後總重")
    bdiff = fields.Integer("桶數差")
    wdiff = fields.Integer("重量差")
    op1 = fields.Many2one("yc.hr", string="操作人員1")
    op2 = fields.Many2one("yc.hr", string="操作人員2")
    op3 = fields.Many2one("yc.hr", string="操作人員3")
    notices1 = fields.Char("注意事項1")
    notices2 = fields.Char("注意事項2")
    notices3 = fields.Char("注意事項3")

    qcnote1 = fields.Char("品管備註1")
    qcnote2 = fields.Char("品管備註2")
    qcnote3 = fields.Char("品管備註3")
    prodnote1 = fields.Char("製造備註1")
    prodnote2 = fields.Char("製造備註2")
    prodnote3 = fields.Char("製造備註3")

    produce_details_ids = fields.Many2many("yc.produce.details")

    @api.onchange("order_furn")
    def _chech_order(self):
        if self._context.get('params')['action'] == 188:
            return {"domain": {"weighted_order": [("order_furn", "=", self.order_furn.id)],
                               "notweighted_order": [("order_furn", "=", self.order_furn.id)]}}

    # @api.onchange('searchname')
    def quantity_review_search_name(self):
        if self._context.get('params')['action'] == 188 and bool(
                self.searchname or self.weighted_order or self.notweighted_order) == True:
            # S05N0200 產量登錄作業
            purchase = self.env["yc.purchase"]
            _name = self.searchname or self.weighted_order.name or self.notweighted_order.name
            _company  = self.env.user.company_id.id
            _id = purchase.search([('name', '=', _name), ('company_id', '=', _company)]).id
            if _id:
                self._display_record(_id)
                details = purchase.search([('id', '=', _id)]).produce_details_ids
                self.produce_details_ids = [(6, _, details.ids)]
            else:
                raise ValidationError(_('沒有這一筆資料'))

    def save_entry_data(self):
        vals = {}
        if self.hidden_name:
            purchase = self.env['yc.purchase'].search([('name', '=', self.hidden_name)])
            # 儲存會異動的就好
            vals.update({'product_code': self.product_code.id, 'batch': self.batch,
                         'norm_code': self.norm_code.id, 'fullorhalf': self.fullorhalf,
                         'txtur_code': self.txtur_code.id, 'surface_code': self.surface_code.id,
                         'proces_code': self.proces_code.id, 'tensihrd': self.tensihrd,
                         'surfhrd': self.surfhrd, 'corehrd': self.corehrd,
                         'carburlayer': self.carburlayer, 'produceday1': self.produceday1,
                         'ptime1': self.ptime1, 'num1': self.num1, 'unit1': self.unit1.id,
                         'num2': self.num2, 'unit2': self.unit2.id, 'num3': self.num3,
                         'unit3': self.unit3.id, 'num4': self.num4, 'unit4': self.unit4.id,
                         'totalpack': self.totalpack, 'pweight': self.pweight,
                         'pre_furn': self.pre_furn, 'feedbucket': self.feedbucket,
                         'feedweight': self.feedweight, 'currnt_furno': self.currnt_furno.id,
                         'weighbuckets': self.weighbuckets, 'tweight': self.tweight,
                         'bdiff': self.bdiff, 'wdiff': self.wdiff, 'op1': self.op1.id,
                         'op2': self.op2.id, 'op3': self.op3.id, 'notices1': self.notices1,
                         'notices2': self.notices1, 'notices3': self.notices3,
                         'qcnote1': self.qcnote1, 'qcnote2': self.qcnote2,
                         'qcnote3': self.qcnote3, 'prodnote1': self.prodnote1,
                         'prodnote2': self.prodnote2, 'prodnote3': self.prodnote3,
                         # 'produce_details_ids': self.produce_details_ids,
                         })
            purchase.write(vals)
            self._display_record(purchase.id)

    def _display_record(self, record_id):
        purchase = self.env["yc.purchase"]
        self.order_furn = None
        self.notweighted_order = None
        self.weighted_order = None
        self.searchname = None
        record = purchase.search([('id', '=', record_id)])
        self.order_name = record.name
        self.hidden_name = record.name
        self.day = record.day
        self.customer_id = record.customer_id
        self.wire_furn = record.wire_furn
        self.product_code = record.product_code
        self.batch = record.batch
        self.norm_code = record.norm_code
        self.fullorhalf = record.fullorhalf
        self.txtur_code = record.txtur_code
        self.surface_code = record.surface_code
        self.proces_code = record.proces_code
        self.tensihrd = record.tensihrd
        self.surfhrd = record.surfhrd
        self.corehrd = record.corehrd
        self.carburlayer = record.carburlayer
        self.produceday1 = record.produceday1
        self.ptime1 = record.ptime1
        self.num1 = record.num1
        self.unit1 = record.unit1
        self.num2 = record.num2
        self.unit2 = record.unit2
        self.num3 = record.num3
        self.unit3 = record.unit3
        self.num4 = record.num4
        self.unit4 = record.unit4
        self.totalpack = record.totalpack
        self.pweight = record.pweight
        self.pre_furn = record.pre_furn
        self.feedbucket = record.feedbucket
        self.feedweight = record.feedweight
        self.currnt_furno = record.currnt_furno
        self.weighbuckets = record.weighbuckets
        self.tweight = record.tweight
        self.bdiff = record.bdiff
        self.wdiff = record.wdiff
        self.op1 = record.op1
        self.op2 = record.op2
        self.op3 = record.op3
        self.notices1 = record.notices1
        self.notices2 = record.notices2
        self.notices3 = record.notices3
        self.qcnote1 = record.qcnote1
        self.qcnote2 = record.qcnote2
        self.qcnote3 = record.qcnote3
        self.prodnote1 = record.prodnote1
        self.prodnote2 = record.prodnote2
        self.prodnote3 = record.prodnote3

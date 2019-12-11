# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime as dt
import pytz

class YcPurchaseDisplay(models.TransientModel):
    _name = 'yc.purchase.process'

    searchname = fields.Char("工令查詢", help="搜尋工令欄位")

    order_name = fields.Char("工令號碼")
    hidden_name = fields.Char("工令號碼")
    furn_in = fields.Many2one("yc.purchase", string="已進爐")
    furn_notin = fields.Many2one("yc.purchase", string="未進爐")
    order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
    day = fields.Date("進貨日期")
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    wire_furn = fields.Char("線材爐號")
    headsign = fields.Binary('頭部記號')
    product_code = fields.Many2one("yc.setproduct", string="品名")
    batch = fields.Char("客戶批號")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    surface_code = fields.Many2one("yc.setsurface", string="表面處理")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    tensihrd = fields.Char("抗拉強度")
    surfhrd = fields.Char("表面硬度")
    corehrd = fields.Char("心部硬度")
    carburlayer = fields.Char("滲碳層")
    produceday1 = fields.Date("製造日期1")
    ptime1 = fields.Char("製造時間1")
    shift1 = fields.Many2one("yc.setshift", string="班別1")
    op1 = fields.Many2one("res.users", string="操作人員1")
    buckets1 = fields.Integer("桶數1")
    pw1 = fields.Integer("製造重量1")
    teamlead1 = fields.Many2one("res.users", string="組長1")
    produceday2 = fields.Date("製造日期2")
    ptime2 = fields.Char("製造時間2")
    shift2 = fields.Many2one("yc.setshift", string="班別2")
    op2 = fields.Many2one("res.users", string="操作人員2")
    buckets2 = fields.Integer("桶數2")
    pw2 = fields.Integer("製造重量2")
    teamlead2 = fields.Many2one("res.users", string="組長2")
    produceday3 = fields.Date("製造日期3")
    ptime3 = fields.Char("製造時間3")
    shift3 = fields.Many2one("yc.setshift", string="班別3")
    op3 = fields.Many2one("res.users", string="操作人員3")
    buckets3 = fields.Integer("桶數3")
    pw3 = fields.Integer("製造重量3")
    teamlead3 = fields.Many2one("res.users", string="組長3")
    ffday = fields.Date("完爐日期")
    fftime = fields.Char("完爐時間")
    num1 = fields.Integer("數量1")
    unit1 = fields.Many2one("yc.setunit", string="單位代號1")
    num2 = fields.Integer("數量2")
    unit2 = fields.Many2one("yc.setunit", string="單位代號2")
    num3 = fields.Integer("數量3")
    unit3 = fields.Many2one("yc.setunit", string="單位代號3")
    num4 = fields.Integer("數量4")
    unit4 = fields.Many2one("yc.setunit", string="單位代號4")
    net = fields.Integer("淨重")
    storeplace = fields.Char("存放位置")
    totalpack = fields.Char("裝袋合計")
    pre_furn = fields.Char("以前爐號")
    currnt_furno = fields.Many2one("yc.setfurnace", string="現在爐號")
    notices1 = fields.Char("注意事項1")
    notices2 = fields.Char("注意事項2")
    notices3 = fields.Char("注意事項3")
    qcnote1 = fields.Char("品管備註1")
    qcnote2 = fields.Char("品管備註2")
    qcnote3 = fields.Char("品管備註3")
    prodnote1 = fields.Char("製造備註1")
    prodnote2 = fields.Char("製造備註2")
    prodnote3 = fields.Char("製造備註3")
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

    produce_details_ids = fields.Many2many("yc.produce.details")

    @api.onchange("order_furn")
    def _chech_order(self):
        _action = self.env['ir.actions.act_window']
        p1 = _action.search([('name', '=', '製程登錄作業')]).id
        if self._context.get('params')['action'] == p1:
            status = self.env['yc.setstatus']
            in_furn = status.search([('name', '=', '己進爐')]).id
            out_of_furn = status.search([('name', '=', '未進爐')]).id
            return {"domain": {"furn_in": [("order_furn", "=", self.order_furn.id), ("status", "=", in_furn)],
                               "furn_notin": [("order_furn", "=", self.order_furn.id), ("status", "=", out_of_furn)]}}

    @api.onchange('searchname', 'furn_in', 'furn_notin')
    def process_review_search_name(self):
        _action = self.env['ir.actions.act_window']
        action_id = _action.search([('name', '=', '製程登錄作業')], limit=1).id
        if self._context.get('params')['action'] == action_id and bool(
                self.searchname or self.furn_in or self.furn_notin) == True:
            # S05N0100 製程登錄作業
            purchase = self.env["yc.purchase"]
            _name = self.searchname or self.furn_in.name or self.furn_notin.name
            # _company = self.env.user.company_id.id
            _id = purchase.search([('name', '=', _name)]).id

            if _id:
                self._display_record(_id)
                now = dt.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d")
                if not self.produceday1:
                    self.produceday1 = now
                if not self.produceday2:
                    self.produceday2 = now
                if not self.produceday3:
                    self.produceday3 = now
                if not self.ffday:
                    self.ffday = now

                # 建好六個空項目檔
                # to_create_order = purchase.search([('id', '=', _id)])
                # if len(to_create_order.produce_details_ids) == 0:
                #     for i in range(1, 7):
                #         # issue: 如果用onchage call只能第六筆，用button才可以完整新增
                #         to_create_order.produce_details_ids = [(0, 0, {'name': _id, 'bucket_no': i})]
                details = purchase.search([('id', '=', _id)]).produce_details_ids
                self.produce_details_ids = [(6, _, details.ids)]
            else:
                raise ValidationError(_('沒有這一筆資料'))

    def save_entry_data(self):
        vals = {}
        if self.hidden_name:
            domain = [('name', '=', self.hidden_name)]
            purchase = self.env['yc.purchase'].search(domain)
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
                         'totalpack': self.totalpack, 'pre_furn': self.pre_furn,
                         'currnt_furno': self.currnt_furno.id, 'op1': self.op1.id,
                         'op2': self.op2.id, 'op3': self.op3.id, 'notices1': self.notices1,
                         'notices2': self.notices1, 'notices3': self.notices3,
                         'qcnote1': self.qcnote1, 'qcnote2': self.qcnote2,
                         'qcnote3': self.qcnote3, 'prodnote1': self.prodnote1,
                         'prodnote2': self.prodnote2, 'prodnote3': self.prodnote3,
                         'headsign': self.headsign, 'strength_level': self.strength_level.id,
                         'shift1': self.shift1.id, 'buckets1': self.buckets1, 'pw1': self.pw1,
                         'teamlead1': self.teamlead1.id, 'produceday2': self.produceday2, 'ptime2': self.ptime2,
                         'shift2': self.shift2.id, 'buckets2': self.buckets2, 'pw2': self.pw2,
                         'teamlead2': self.teamlead2.id, 'produceday3': self.produceday3, 'ptime3': self.ptime3,
                         'shift3': self.shift3.id, 'buckets3': self.buckets3, 'pw3': self.pw3,
                         'teamlead3': self.teamlead3.id, 'ffday': self.ffday, 'fftime': self.fftime,
                         'net': self.net, 'storeplace': self.storeplace, 'flow': self.flow, 'cp': self.cp,
                         'nh31': self.nh31, 'nh32': self.nh32, 'nh33': self.nh33, 'nh34': self.nh34,
                         'heat1': self.heat1, 'heat2': self.heat2, 'heat3': self.heat3, 'heat4': self.heat4,
                         'heat5': self.heat5, 'heat6': self.heat6, 'heat7': self.heat7, 'heat8': self.heat8,
                         'heattemp': self.heattemp, 'heatsped': self.heatsped, 'tempturing1': self.tempturing1,
                         'tempturing2': self.tempturing2, 'tempturing3': self.tempturing3,
                         'tempturing4': self.tempturing4,
                         'tempturing5': self.tempturing5, 'tempturing6': self.tempturing6,
                         'tempturisped': self.tempturisped,
                         })
            if vals.get('ptime1') != '':
                infurn_code = self.env['yc.setstatus'].search([('name', '=', '己進爐')]).id
                vals.update({'status': infurn_code})
            else:
                not_infurn_code = self.env['yc.setstatus'].search([('name', '=', '未進爐')]).id
                vals.update({'status': not_infurn_code})
            purchase.write(vals)
            self._display_record(purchase.id)

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
        _name = self.hidden_name
        # _company = self.env.user.company_id.id
        to_clear_id = db.search([('name', '=', _name)]).id
        vals = {}
        for field in to_clear_field:
            vals.update({field: None})
        db.search([('id', '=', to_clear_id)]).write({vals})
        self._display_record(to_clear_id)

    def _display_record(self, record_id):
        # TODO: getattrs and setattrs method to overwrite this.
        purchase = self.env["yc.purchase"]
        self.order_furn = None
        self.notweighted_order = None
        self.weighted_order = None
        self.searchname = None
        self.furn_in = None
        self.furn_notin = None
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
        self.pre_furn = record.pre_furn
        self.currnt_furno = record.currnt_furno
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
        self.headsign = record.headsign
        self.strength_level = record.strength_level
        self.shift1 = record.shift1
        self.buckets1 = record.buckets1
        self.pw1 = record.pw1
        self.teamlead1 = record.teamlead1
        self.produceday2 = record.produceday2
        self.ptime2 = record.ptime2
        self.shift2 = record.shift2
        self.buckets2 = record.buckets2
        self.pw2 = record.pw2
        self.teamlead2 = record.teamlead2
        self.produceday3 = record.produceday3
        self.ptime3 = record.ptime3
        self.shift3 = record.shift3
        self.buckets3 = record.buckets3
        self.pw3 = record.pw3
        self.teamlead3 = record.teamlead3
        self.ffday = record.ffday
        self.fftime = record.fftime
        self.net = record.net
        self.storeplace = record.storeplace
        self.flow = record.flow
        self.cp = record.cp
        self.nh31 = record.nh31
        self.nh32 = record.nh32
        self.nh33 = record.nh33
        self.nh34 = record.nh34
        self.heat1 = record.heat1
        self.heat2 = record.heat2
        self.heat3 = record.heat3
        self.heat4 = record.heat4
        self.heat5 = record.heat5
        self.heat6 = record.heat6
        self.heat7 = record.heat7
        self.heat8 = record.heat8
        self.heattemp = record.heattemp
        self.heatsped = record.heatsped
        self.tempturing1 = record.tempturing1
        self.tempturing2 = record.tempturing2
        self.tempturing3 = record.tempturing3
        self.tempturing4 = record.tempturing4
        self.tempturing5 = record.tempturing5
        self.tempturing6 = record.tempturing6

    def plus_one_line(self):
        if self.hidden_name:
            purchase = self.env['yc.purchase']
            _no = len(self.produce_details_ids)
            # to_create_order = purchase.search([('id', '=', _id)])
            # to_create_order.produce_details_ids = [(0, 0, {'name': _id, 'bucket_no': i})]
            _id = purchase.search([('name', '=', self.hidden_name)]).id
            record = purchase.search([('id', '=', _id)])
            record.produce_details_ids = [(0, 0, {'name': _id, 'bucket_no': _no+1})]
            self.produce_details_ids = [(6, _, record.produce_details_ids.ids)]

    def delete_last_line(self):
        if self.hidden_name:
            _no = len(self.produce_details_ids)
            if _no ==0:
                raise ValidationError(_('沒東西刪了'))
            else:
                _id = self.produce_details_ids[0].name.id
                purchase = self.env['yc.purchase']
                detail = self.env['yc.produce.details']
                record = purchase.search([('id', '=', _id)])
                _delete_id = detail.search([('name', '=', _id), ('bucket_no', '=', _no)])
                # 再create狀態無法使用
                _delete_id.unlink()
                self.produce_details_ids = [(6, _, record.produce_details_ids.ids)]


    p1 = fields.Boolean()
    p2 = fields.Boolean()
    p3 = fields.Boolean()
    @api.onchange('p1')
    def cokoo1(self):
        if self.hidden_name: # 避免空畫面自動load
            now = dt.now(pytz.timezone('Asia/Taipei')).strftime("%Y%m%d%H%M%S")
            time = '%s:%s' % (now[8:10], now[10:12])
            self.ptime1 = time
            self.save_entry_data()

    @api.onchange('p2')
    def cokoo2(self):
        if self.hidden_name:
            now = dt.now(pytz.timezone('Asia/Taipei')).strftime("%Y%m%d%H%M%S")
            time = '%s:%s' % (now[8:10], now[10:12])
            self.ptime2 = time
            self.save_entry_data()

    @api.onchange('p3')
    def cokoo3(self):
        if self.hidden_name:
            now = dt.now(pytz.timezone('Asia/Taipei')).strftime("%Y%m%d%H%M%S")
            time = '%s:%s' % (now[8:10], now[10:12])
            self.ptime3 = time
            self.save_entry_data()



# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YcPurchaseDisplay(models.TransientModel):
    _name = 'yc.purchase.display'
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    order_furn = fields.Many2one("yc.setfurnace", string="爐號")
    order_furn2 = fields.Many2one("yc.setfurnace", string="爐號")
    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")
    purchase_ids2 = fields.Many2many("yc.purchase", relation='yc_purchase_yc_purchase_display_rel2',
                                     string="purchase search", help="查詢列表")
    records_number = fields.Char("資料筆數", default='共　筆資料')
    records_number2 = fields.Char("資料筆數", default='共　筆資料')
    record_limit = fields.Integer("資料限制筆數", default=200, help="限制資料筆數")

    # page1: 分爐排程
    @api.onchange("customer_id", "order_furn")
    def _filter_order(self):
        if self.customer_id or self.order_furn:
            # 先清空list
            domain = ()
            if self.customer_id:
                domain += ('customer_id', '=', self.customer_id.id),
            if self.order_furn:
                domain += ('order_furn', '=', self.order_furn.id),
            if len(domain) > 0:
                # 已出貨
                shiped = self.env['yc.setstatus'].search([('name', '=', '已出貨')]).id
                # domain += ('company_id', '=', self.env.user.company_id.id),
                domain += ('status', '!=', shiped),
                purchase = self.env["yc.purchase"]
                records = purchase.search([d for d in domain], limit=self.record_limit)
                if len(records) == 0:
                    self.records_number = '找不到資料'
                else:
                    self.records_number = '共 %d 筆資料' % len(records)
                self.purchase_ids = [(6, 0, records.ids)]

    @api.onchange("purchase_ids")
    def _update_order(self):
        if self.purchase_ids:
            # 要怎麼找到異動的那一筆id並更新? or 只能每一筆都更新?
            # issue: 異動完 查詢該爐號會出現改筆異動資料 但顯示爐號仍為修正前狀態(實際已修正) 但Refresh 後ok
            vals = {}
            for rec in self.purchase_ids:
                # self.purchase_ids = [(1, rec.id, {'order_furn': rec.order_furn.id})] seems can't not use in create
                vals.update({'order_furn': rec.order_furn.id})
                purchase = self.env["yc.purchase"]
                purchase.search([('id', '=', rec.id)]).write(vals)
            self._filter_order()

    # page2: 爐內進貨
    @api.onchange("order_furn2")
    def _filter_order2(self):
        if self.order_furn2:
            domain = ()
            domain += ('order_furn', '=', self.order_furn2.id),
            if len(domain) > 0:
                # 排除已出貨
                shiped = self.env['yc.setstatus'].search([('name', '=', '已出貨')]).id
                # domain += ('company_id', '=', self.env.user.company_id.id),
                domain += ('status', '!=', shiped),
                purchase = self.env["yc.purchase"]
                records = purchase.search([d for d in domain], order='serial', limit=self.record_limit)
                if len(records) == 0:
                    self.records_number2 = '找不到資料'
                else:
                    self.records_number2 = '共 %d 筆資料' % len(records)
                self.purchase_ids2 = [(6, 0, records.ids)]

    # 修改加熱爐2要連同修正其他加熱爐
    @api.onchange('purchase_ids2')
    def _update_tempt(self):
        # 還不知道怎麼鑑別是改哪一筆資料前全部修正一遍
        if self.purchase_ids2:
            vals = {}
            purchase = self.env['yc.purchase']
            for record in self.purchase_ids2:
                init = int(record.tempturing2)
                vals.update({'tempturing1': init - 30, 'tempturing3': init,
                             'tempturing4': init, 'tempturing5': init,
                             'tempturing6': init, 'tempturing7': init,
                             'tempturing8': init})
                purchase.search([('id', '=', record.id)]).write(vals)

    def form_refresh(self):
        if self.purchase_ids2:
            vals = {}
            sort_list = []
            purchase = self.env["yc.purchase"]
            # 重新排序要排除99.9、非登入廠、已出貨
            shiped = self.env['yc.setstatus'].search([('name', '=', '已出貨')]).id
            unscheduled = self.env['yc.setstatus'].search([('name', '=', '未排程')]).id
            _domain = ()
            _domain += ('order_furn', '=', self.order_furn2.id),
            # _domain += ('company_id', '=', self.env.user.company_id.id),
            _domain += ('status', '!=', shiped),
            _domain_unscheduled, _domain__scheduled = _domain, _domain
            _domain_unscheduled += (('serial', '=', 99.9)),
            _domain__scheduled += (('serial', '!=', 99.9)),
            rows_for_unscheduled = self.purchase_ids2.search([d for d in _domain_unscheduled])
            rows_for_schedule = self.purchase_ids2.search([d for d in _domain__scheduled])
            # 先將99.9 狀態要改成未排程
            for row in rows_for_unscheduled:
                vals.update({'status': unscheduled})
                purchase.search([('id', '=', row.id)]).write(vals)
            # 重新排序、狀態改成未進爐
            for row in rows_for_schedule:
                sort_list.append([row.id, row.serial])
            sort_list.sort(key=lambda list: list[1])
            for x in range(len(sort_list)):
                sort_list[x][1] = x + 1
                not_infurn = self.env['yc.setstatus'].search([('name', '=', '未進爐')]).id
                vals.update({'serial': sort_list[x][1],
                             'status': not_infurn})
                # [(1, id, vals)] 好像無法用在create狀態
                purchase.search([('id', '=', sort_list[x][0])]).write(vals)
        self._filter_order()
        self._filter_order2()

    # def clear_records(self):
    #     self.purchase_ids = [(5, 0, 0)]
    #     self.purchase_ids2 = [(5, 0, 0)]

# class YcPurchaseDisplayWizard(models.TransientModel):
#     _name="yc.purchase.display.wizard"
#
#     name = fields.Char("工令號碼")
#     day = fields.Date("進貨日期")
#     customer_id = fields.Many2one("yc.customer", "客戶名稱")
#     batch = fields.Char("客戶批號")
#     product_code = fields.Many2one("yc.setproduct", string="品名", index=True, auto_join=True)
#     norm_code = fields.Many2one("yc.setnorm", string="規格")
#     len_code = fields.Many2one("yc.setlength", string="長度")
#     len_descript = fields.Char("長度說明")
#     clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
#     txtur_code = fields.Many2one("yc.settexture", string="材質")
#     surface_code = fields.Many2one("yc.setsurface", string="表面處理")
#     strength_level = fields.Many2one("yc.setstrength", string="強度級數")
#     fullorhalf = fields.Selection([('半牙', '半牙'), ('全牙', '全牙'), ('無', '無')], '全或半牙')
#     proces_code = fields.Many2one("yc.setprocess", string="加工方式")
#     num1 = fields.Integer("數量1")
#     unit1 = fields.Many2one("yc.setunit", string="單位代號1")
#     num2 = fields.Integer("數量2")
#     unit2 = fields.Many2one("yc.setunit", string="單位代號2")
#     num3 = fields.Integer("數量3")
#     unit3 = fields.Many2one("yc.setunit", string="單位代號3")
#     num4 = fields.Integer("數量4")
#     unit4 = fields.Many2one("yc.setunit", string="單位代號4")
#     net = fields.Integer("淨重")
#     surfhrd = fields.Char("表面硬度")
#     corehrd = fields.Char("心部硬度")
#     storeplace = fields.Char("存放位置")
#     tensihrd = fields.Char("抗拉強度")
#     carburlayer = fields.Char("滲碳層")
#     order_furn = fields.Many2one("yc.setfurnace", string="預排爐號")
#     wire_furn = fields.Char("線材爐號")
#     produceday1 = fields.Date("製造日期1")
#     shift1 = fields.Many2one("yc.setshift", string="班別1")
#     op1 = fields.Many2one("yc.hr", string="操作人員1")
#     ptime1 = fields.Char("製造時間1")
#     qc = fields.Many2one("yc.hr", string="品管人員")
#     flow = fields.Char("流量")
#     cp = fields.Char("CP值")
#     nh31 = fields.Char("氨值1")
#     nh32 = fields.Char("氨值2")
#     nh33 = fields.Char("氨值3")
#     nh34 = fields.Char("氨值4")
#     heat1 = fields.Char("加熱爐1")
#     heat2 = fields.Char("加熱爐2")
#     heat3 = fields.Char("加熱爐3")
#     heat4 = fields.Char("加熱爐4")
#     heat5 = fields.Char("加熱爐5")
#     heat6 = fields.Char("加熱爐6")
#     heat7 = fields.Char("加熱爐7")
#     heat8 = fields.Char("加熱爐8")
#     heattemp = fields.Char("加熱爐油溫")
#     heatsped = fields.Char("加熱爐速度")
#     tempturing1 = fields.Char("回火爐1")
#     tempturing2 = fields.Char("回火爐2")
#     tempturing3 = fields.Char("回火爐3")
#     tempturing4 = fields.Char("回火爐4")
#     tempturing5 = fields.Char("回火爐5")
#     tempturing6 = fields.Char("回火爐6")
#     tempturisped = fields.Char("回火爐速度")
#     notices1 = fields.Char("注意事項1")
#     notices2 = fields.Char("注意事項2")
#     notices3 = fields.Char("注意事項3")
#     qcnote1 = fields.Char("品管備註1")
#     qcnote2 = fields.Char("品管備註2")
#     qcnote3 = fields.Char("品管備註3")
#     prodnote1 = fields.Char("製造備註1")
#     prodnote2 = fields.Char("製造備註2")
#     prodnote3 = fields.Char("製造備註3")

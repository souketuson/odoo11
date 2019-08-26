# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime as dt


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

    def call_furna_order(self):
        if self.purchase_ids2:
            records = self.purchase_ids2

            data = {
                'ids': records.ids,
                'model': self._name,
                'furn': self.order_furn2.name,
                'form': {

                },
            }
            # use `module_name.report_id` as reference.
            # `report_action()` will call `get_report_values()` and pass `data` automatically.
            return self.env.ref('yc_root.action_furna_order').report_action(self, data=data)

class YcFurnaOrderReport(models.AbstractModel):
    '''restrict form "report.module_name.template_id"'''
    _name = 'report.yc_root.report_furna_order'

    @api.model
    def get_report_values(self, docids, data=None):
        _ids = data['ids']

        purchase = self.env['yc.purchase']
        docs = []
        for i in _ids:
            r = purchase.browse(i)
            docs.append({
                'name': r.name,
                'customer_id': r.customer_id.name,
                'product_code':r.product_code.name,
                # 'produceday': r.produceday,
                'norm_code':r.norm_code.name,
                'len_code':r.len_code.name,
                'len_descript': r.len_descript,
                'txtur_code':r.txtur_code.name,
                # 'wire_furn':r.wire_furn,
                'num1':r.num1,
                'unit1':r.unit1.name,
                'proces_code':r.proces_code.name,
                # 'surface_code':r.surface_code.name,
                'elecpl_code':r.elecpl_code.name,
                'batch':r.batch,
                'surfhrd':r.surfhrd,
                'corehrd':r.corehrd,
                # 'carburlayer':r.carburlayer,
                # 'tensihrd':r.tensihrd,
                # 'torsion':r.torsion,
                'day':r.day,
                # 'ck_person':r.ck_person.name,
                'process1': r.process1.abbrev,
                'storeplace_id': r.storeplace_id.name,
                'notices1': r.notices1,
                'notices2': r.notices2,
                'notices3': r.notices3,
                'net': r.net,
                'cp': r.cp,
                'flow': r.flow,
                'heatsped': r.heatsped,
                'heattemp': r.heattemp,
                'heat1': r.heat1,
                'heat2': r.heat2,
                'heat3': r.heat3,
                'heat4': r.heat4,
                'heat5': r.heat5,
                'heat6': r.heat6,
                'heat7': r.heat7,
                'heat8': r.heat8,
                'tempturing1': r.tempturing1,
                'tempturing2': r.tempturing2,
                'tempturing3': r.tempturing3,
                'tempturing4': r.tempturing4,
                'tempturing5': r.tempturing5,
                'tempturing6': r.tempturing6,
                'tempturisped': r.tempturisped,
            })
        return {'doc_ids': _ids,
                'doc_model': 'yc.purchase',
                'doc_furn': data['furn'],
                'doc_day': dt.today().strftime('%Y/%m/%d'),
                'docs': docs}

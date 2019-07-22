# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class YcPurchaseWizard(models.TransientModel):
    _name = 'yc.purchase.wizard'

    ck1 = fields.Boolean("品名check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    product_code = fields.Many2one("yc.setproduct", string="品名")
    ck4 = fields.Boolean("品名分類check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    productname = fields.Many2one("yc.setproduct", string="產品名稱")
    ck2 = fields.Boolean("規格check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    ck5 = fields.Boolean("加工方式check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    ck3 = fields.Boolean("長度check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    len_code = fields.Many2one("yc.setlength", string="長度")
    ck6 = fields.Boolean("材質check", default=True)
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    ck7 = fields.Boolean("強度級數check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    ck8 = fields.Boolean("線材爐號check", default=True, help="在搜尋舊檔wizard自動代入篩選")
    wire_furn = fields.Char("線材爐號")
    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")
    rec_number = fields.Char("資料筆數", readonly=True)
    initial = fields.Boolean(default=True)

    @api.onchange('initial')
    def _initial(self):
        source = self.env['yc.purchase'].browse(self._context.get('active_ids'))
        self.product_code = source.product_code
        self.norm_code = source.norm_code
        self.len_code = source.len_code
        self.clsf_code = source.clsf_code
        self.proces_code = source.proces_code
        self.txtur_code = source.txtur_code
        self.strength_level = source.strength_level
        self.wire_furn = source.wire_furn

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
        self.search_purchase()




    # 過濾查詢條件
    @api.onchange('product_code', 'clsf_code', 'productname', 'norm_code',
                  'proces_code', 'len_code', 'txtur_code', 'strength_level', 'wire_furn')
    def search_purchase(self):
        # 剛載入執行
        source = self.env['yc.purchase'].browse(self._context.get('active_ids'))
        # 如果wizard有任意欄位有值
        if (self.product_code or self.clsf_code or self.productname or self.norm_code or self.proces_code or
                self.len_code or self.txtur_code or self.strength_level or self.wire_furn):
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
                purchase = self.env['yc.purchase']
                # 搜尋出來的list要排除掉自己
                domain += ('id', '!=', source.id),
                records = purchase.search([d for d in domain])
                # 搜尋並列表
                if len(records) > 0:
                    self.purchase_ids = [(4, record.id) for record in records]
                    self.rec_number = ""
                else:
                    self.purchase_ids = None
                    self.rec_number = "找不到資料"
        else:
            self.purchase_ids = None
            self.rec_number = "請勾選並依查詢下拉選擇品項"


    # 把表面硬度,心部硬度,試片,抗拉強度,滲碳層,以前爐號,扭力,回火溫度,預排爐號 帶入到現在的進貨單
    @api.multi
    def comfirm(self):
        checked = self.purchase_ids.search([('wizard_check', '=', True)])
        if len(checked) > 1:
            for to_uncheck in checked:
                to_uncheck.wizard_check = False
            raise Warning("只能選一筆資料帶出")
        if len(checked) == 1:
            # 解掉checked
            checked.wizard_check = False
            # 目前進貨單current record : self._context.get('active_ids')
            current = self.env['yc.purchase'].browse(self._context.get('active_ids'))
            current.surfhrd = checked.surfhrd
            current.corehrd = checked.corehrd
            current.piece = checked.piece
            current.tensihrd = checked.tensihrd
            current.carburlayer = checked.carburlayer
            current.torsion = checked.torsion
            current.tempturing2 = checked.tempturing2
            current.order_furn = checked.order_furn
            if self.product_code and self.ck1:
                current.product_code = self.product_code
            if self.clsf_code and self.ck4:
                current.clsf_code = self.clsf_code
            if self.norm_code and self.ck2:
                current.norm_code = self.norm_code
            if self.proces_code and self.ck5:
                current.proces_code = self.proces_code
            if self.len_code and self.ck3:
                current.len_code = self.len_code
            if self.txtur_code and self.ck6:
                current.txtur_code = self.txtur_code
            if self.strength_level and self.ck7:
                current.strength_level = self.strength_level
            if self.wire_furn and self.ck8:
                current.wire_furn = self.wire_furn




class YcYcPurchasePreorder(models.TransientModel):
    _name = 'yc.purchase.preorder'

    condition = fields.Selection([('IT', '廠內退回'), ('OT', '廠外退回')],
                                 string="退回來源")
    return_ids = fields.Many2many("yc.return", string="purchase search", help="查詢列表")
    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")

    @api.onchange('condition')
    def search_purchase(self):
        if self.condition:
            transmit_code = self.env['yc.setstatus'].search([('name', '=', '轉廠')]).id
            # 要先建好出貨退回檔
            # OT_list = [(name) for name in self.env['轉廠單項目檔'].search([]).name ]
            if self.condition == 'OT':
                records = self.env['yc.return'].search([])
                self.return_ids = [(4, record.id) for record in records]
            elif self.condition == 'IT':
                # 廠內退回似乎在品質檢驗階段 如果被轉入進貨單 前工令單會自動key值
                # IT 只要找出前工令號有值 and 等於工令號的紀錄
                has_preorder = self.env['yc.purchase'].search([("pre_order", '!=', '')])
                self.purchase_ids = [(4, rec.id) for rec in has_preorder]

    def comfirm(self):
        # 先判斷要帶出退回來源
        # 拉出的工令其工令名應該要產生新的，否則在製造或產量檢視表會出現錯誤
        # 項目檔應該先清空
        p_cked = self.purchase_ids.search([('wizard_check', '=', True)])
        r_cked = self.return_ids.search([('wizard_check', '=', True)])
        purchase = self.env['yc.purchase']

        if self.condition == 'IT':
            p_cked.wizard_check = False
            if len(p_cked) > 1:
                raise ValidationError((_('只能帶一筆')))
            else:
                _id = self._context.get('active_ids')
                new_order = purchase.search([('id', '=', _id)])
                # 把欄位名稱都讀出來 self._proper_fields._map.keys()
                # for loop: a.write({k :b['dic.key']})
                _fields = []
                vals = {}
                for key in p_cked._proper_fields._map.keys():
                    _fields.append(key)
                for _f in _fields:
                    # M2O has attr 'id'
                    if hasattr(p_cked[_f], 'id'):
                        vals.update({_f: p_cked[_f].id})
                    else:
                        if _f == 'name':
                            vals.update({_f: 'r' + p_cked[_f]})
                        else:
                            vals.update({_f: p_cked[_f]})
                new_order.write(vals)

        elif self.condition == 'OT':
            r_cked.wizard_check = False
            if len(r_cked) > 1:
                raise ValidationError((_('只能帶一筆')))
            else:
                _id = self._context.get('active_ids')
                new_order = purchase.search([('id', '=', _id)])
                res_order = purchase.search([('name', '=', r_cked.name)])
                _fields = []
                vals = {}
                for key in res_order._proper_fields._map.keys():
                    _fields.append(key)
                for _f in _fields:
                    if hasattr(res_order[_f], 'id'):
                        if _f == 'produce_details_ids':
                            vals.update({_f: False})
                        else:
                            vals.update({_f: res_order[_f].id})
                    else:
                        if _f == 'name':
                            vals.update({_f: 'r' + res_order[_f]})
                        else:
                            vals.update({_f: res_order[_f]})
                    new_order.write(vals)
        return

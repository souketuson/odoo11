from odoo import models, fields, api


class YcPurchaseDisplay(models.TransientModel):
    _name = 'yc.purchase.display'
    customer_id = fields.Many2one("yc.customer", "客戶名稱")
    order_furn = fields.Many2one("yc.setfurnace", string="爐號")
    order_furn2 = fields.Many2one("yc.setfurnace", string="爐號")
    purchase_ids = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")
    purchase_ids2 = fields.Many2many("yc.purchase", string="purchase search", help="查詢列表")
    records_number = fields.Char("資料筆數", default='共　筆資料')
    records_number2 = fields.Char("資料筆數", default='共　筆資料')
    record_limit = fields.Integer("資料限制筆數", default=100)
    # issue: 目前填完爐號按Enter 會跳出wizard 要如何取消?
    # 2 如何更新x2many?
    # page1: 分爐排程
    @api.onchange("customer_id", "order_furn")
    def _filter_order(self):
        domain = ()
        if self.customer_id:
            domain += ('customer_id', '=', self.customer_id.id),
        if self.order_furn:
            domain += ('order_furn', '=', self.order_furn.id ),
        if len(domain) > 0:
            purchase = self.env["yc.purchase"]
            records = purchase.search([(d) for d in domain], limit= self.record_limit)
            if len(records) == 0:
                self.records_number = '找不到資料'
            else:
                self.records_number = '共 %d 筆資料' % len(records)
            for rec in self:
                rec.purchase_ids = [(4, record.id) for record in records]

    @api.onchange("purchase_ids")
    def _update_x2many(self):
        if self.purchase_ids:
            # 要怎麼找到異動的那一筆id並更新? or 只能每一筆都更新?
            # issue: 異動完 查詢該爐號會出現改筆異動資料 但顯示爐號仍為修正前狀態(實際已修正)
            vals = {}
            for rec in self.purchase_ids:
                # self.purchase_ids = [(1, rec.id, {'order_furn': rec.order_furn.id})] seems can't not use in create
                vals.update({'order_furn': rec.order_furn.id})
                purchase = self.env["yc.purchase"]
                purchase.search([('id','=', rec.id)]).write(vals)
            self._filter_order()

    # page2: 爐內進貨
    @api.onchange("order_furn2")
    def _filter_order2(self):
        domain = ()
        if self.order_furn2:
            domain += ('order_furn', '=', self.order_furn2.id),

        if len(domain) > 0:
            purchase = self.env["yc.purchase"]
            records = purchase.search([(d) for d in domain], order='serial', limit= self.record_limit)
            if len(records) == 0:
                self.records_number2 = '找不到資料'
            else:
                self.records_number2 = '共 %d 筆資料' % len(records)
            for rec in self:
                rec.purchase_ids2 = [(4, record.id) for record in records]
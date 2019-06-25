# -*- coding: utf-8 -*-


from odoo import models, fields, api


class YcBusiness(models.Model):
    _name = "yc.customer"
    _rec_name = "abbrev"

    code = fields.Char("客戶編號")
    name = fields.Char("客戶名稱")
    abbrev = fields.Char("簡稱")
    contact = fields.Char("負責人")
    cls_code = fields.Char("分類代碼")
    taxid = fields.Char("統一編號")
    title = fields.Char("公司抬頭")
    post_code = fields.Char("公司郵遞區號")
    address = fields.Char("公司地址")
    mpost_code = fields.Char("帳單郵遞區號")
    maddress = fields.Char("帳單地址")
    phone1 = fields.Char("電話")
    phone2 = fields.Char("電話2")
    phone3 = fields.Char("電話3")
    fax1 = fields.Char("傳真1")
    fax2 = fields.Char("傳真2")
    website = fields.Char("網址")
    email = fields.Text("E_Mail")
    note1 = fields.Text("備註1")
    note2 = fields.Text("備註2")
    note3 = fields.Text("備註3")
    note4 = fields.Text("備註4")
    note5 = fields.Text("備註5")
    note6 = fields.Text("備註6")
    note7 = fields.Text("備註7")
    note8 = fields.Text("備註8")
    note9 = fields.Text("備註9")
    note10 = fields.Text("備註10")
    testyet = fields.Char("試片否")
    contactornot = fields.Char("往來否")
    opost_code1 = fields.Char("其他郵遞區號1")
    oaddress1 = fields.Char("其他地址1")
    opost_code2 = fields.Char("其他郵遞區號2")
    oaddress2 = fields.Char("其他地址2")
    opost_code3 = fields.Char("其他郵遞區號3")
    oaddress3 = fields.Char("其他地址3")

    @api.multi
    def name_get(self):
        # <field name="customer_id" context="{'type': 'display'}"/>
        if self._context.get('type') == 'display':
            return [(record.id, "%s %s" % (record.code, record.name)) for record in self]
        else:
            return [(record.id, record.name) for record in self]

    # 讓many2one下拉可以搜尋"代碼"來找產品
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if u'\u4e00' <= name <= u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        customer = self.search(domain + args, limit=limit)
        return customer.name_get()


class YcProcessing(models.Model):
    _name = "yc.processing"

    code = fields.Char("加工廠編號")
    name = fields.Char("加工廠名稱")
    type = fields.Selection([('A', 'A type'), ('B', 'B type')], '加工廠類型')
    cls_code = fields.Char("分類代碼")
    locate_code = fields.Char("區域代碼")
    taxid = fields.Char("統一編號")
    abbrev = fields.Char("簡稱")
    contact = fields.Char("負責人")

    title = fields.Char("公司抬頭")
    post_code = fields.Char("營業郵遞區號")
    address = fields.Char("營業地址")
    bpost_code = fields.Char("帳單郵遞區號")
    baddress = fields.Char("帳單地址")
    fpost_code = fields.Char("工廠郵遞區號")
    faddress = fields.Char("工廠地址")
    phone1 = fields.Char("電話")
    phone2 = fields.Char("電話2")
    phone3 = fields.Char("電話3")
    fax1 = fields.Char("傳真1")
    fax2 = fields.Char("傳真2")
    fphone1 = fields.Char("工廠電話1")
    ffax1 = fields.Char("工廠傳真1")
    website = fields.Char("網址")
    email = fields.Char("E_Mail")
    item = fields.Text("產品項目")
    note1 = fields.Text("備註1")
    note2 = fields.Text("備註2")
    note3 = fields.Text("備註3")
    note4 = fields.Text("備註4")
    note5 = fields.Text("備註5")
    note6 = fields.Text("備註6")
    note7 = fields.Text("備註7")
    note8 = fields.Text("備註8")
    note9 = fields.Text("備註9")
    note10 = fields.Text("備註10")


class YcSupplier(models.Model):
    _name = "yc.supplier"

    name = fields.Char("廠商名稱")
    code = fields.Char("廠商代號")
    cls_code = fields.Char("分類代碼")
    taxid = fields.Char("統一編號")
    contact = fields.Char("負責人")
    title = fields.Char("公司抬頭")
    abbrev = fields.Char("簡稱")
    contactornot = fields.Char("往來否")
    post_code = fields.Char("營業郵遞區號")
    address = fields.Char("營業地址")
    bpost_code = fields.Char("帳單郵遞區號")
    baddress = fields.Char("帳單地址")
    fpost_code = fields.Char("工廠郵遞區號")
    faddress = fields.Char("工廠地址")
    phone1 = fields.Char("電話")
    fax1 = fields.Char("傳真1")
    fphone1 = fields.Char("工廠電話1")
    ffax1 = fields.Char("工廠傳真1")
    website = fields.Char("網址")
    email = fields.Char("E_Mail")
    item = fields.Text("產品項目")
    note1 = fields.Text("備註1")
    note2 = fields.Text("備註2")
    note3 = fields.Text("備註3")
    note4 = fields.Text("備註4")
    note5 = fields.Text("備註5")
    note6 = fields.Text("備註6")
    note7 = fields.Text("備註7")
    note8 = fields.Text("備註8")
    note9 = fields.Text("備註9")
    note10 = fields.Text("備註10")
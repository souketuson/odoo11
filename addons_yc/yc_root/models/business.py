# -*- coding: utf-8 -*-


from odoo import models, fields, api


class YcBusiness(models.Model):
    _name = "yc.customer"
    _rec_name = "abbrev"

    code = fields.Char("客戶編號")
    name = fields.Char("客戶名稱")
    abbrev = fields.Char("簡稱")
    phone = fields.Char("電話")
    contact = fields.Char("負責人")
    cls_code = fields.Char("分類代碼")
    taxid = fields.Char("統一編號")
    title = fields.Char("公司抬頭")
    postcode = fields.Char("公司郵遞區號")
    address = fields.Char("公司地址")
    billpostcode = fields.Char("帳單郵遞區號")
    billaddress = fields.Char("帳單地址")
    phone1 = fields.Char("電話1")
    phone2 = fields.Char("電話2")
    phone3 = fields.Char("電話3")
    fax1 = fields.Char("傳真1")
    fax2 = fields.Char("傳真2")
    website = fields.Char("網址")
    email = fields.Char("E_Mail")
    note1 = fields.Char("備註1")
    note2 = fields.Char("備註2")
    note3 = fields.Char("備註3")
    note4 = fields.Char("備註4")
    note5 = fields.Char("備註5")
    note6 = fields.Char("備註6")
    note7 = fields.Char("備註7")
    note8 = fields.Char("備註8")
    note9 = fields.Char("備註9")
    note10 = fields.Char("備註10")
    testyet = fields.Char("試片否")
    contactornot = fields.Char("往來否")
    otherpostcode1 = fields.Char("其他郵遞區號1")
    otheraddress1 = fields.Char("其他地址1")
    otherpostcode2 = fields.Char("其他郵遞區號2")
    otheraddress2 = fields.Char("其他地址2")
    otherpostcode3 = fields.Char("其他郵遞區號3")
    otheraddress3 = fields.Char("其他地址3")


class YcProcessing(models.Model):
    _name = "yc.processing"

    code = fields.Char("加工廠編號")
    name = fields.Char("加工廠名稱")
    phone = fields.Char("電話")
    contact = fields.Char("負責人")

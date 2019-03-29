# -*- coding: utf-8 -*-


from odoo import models, fields


class YcSetstrength(models.Model):
    # 強度級數 S03N0002
    _name = "yc.setstrength"
    name = fields.Char("強度名稱")
    code = fields.Char("強度代碼")


class YcSetproductclassify(models.Model):
    # 產品分類 S03N0003
    _name = "yc.setproductclassify"
    name = fields.Char("分類名稱")
    code = fields.Char("分類代碼")


class YcSetnorm(models.Model):
    # 規格 S03N0004
    _name = "yc.setnorm"
    name = fields.Char("規格名稱")
    code = fields.Char("規格代碼")
    parmeter1 = fields.Char("參數1")
    parmeter2 = fields.Char("參數2")
    parmeter3 = fields.Char("參數3")


class YcSetlength(models.Model):
    # 長度 S03N0005
    _name = "yc.setlength"
    name = fields.Char("長度名稱")
    code = fields.Char("長度代碼")


class YcSetprocess(models.Model):
    #  加工方式 S03N0006
    _name = "yc.setprocess"
    name = fields.Char("加工方式")
    code = fields.Char("加工方式代碼")


class YcSettexture(models.Model):
    # 材質 S03N0007
    _name = "yc.settexture"
    name = fields.Char("材質名稱")
    code = fields.Char("材質代碼")


class YcSetsurface(models.Model):
    # 表面處理 S03N0008
    _name = "yc.setsurface"
    name = fields.Char("表面處理名稱")
    code = fields.Char("表面處理代碼")


class YcSetelectroplating(models.Model):
    # 電鍍 S03N0009
    _name = "yc.setelectroplating"
    name = fields.Char("電鍍名稱")
    code = fields.Char("電鍍代碼")


class YcSeteunit(models.Model):
    # 單位 S03N0011
    _name = "yc.setunit"
    name = fields.Char("單位名稱")
    code = fields.Char("單位代碼")

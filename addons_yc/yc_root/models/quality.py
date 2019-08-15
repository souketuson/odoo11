from odoo import models, fields, api
from datetime import datetime as dt


class YcMechanicalproperty(models.Model):
    _name = "yc.mechanicalproperty"

    name = fields.Char("編號")
    standard = fields.Char("依據標準")
    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    stdcodeinit = fields.Char("規格代碼起")
    stdcodeend = fields.Char("規格代碼訖")
    stdreviewinit = fields.Float("規格對照起")
    stdreviewend = fields.Float("規格對照訖")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    surfaceform = fields.Char("表面規格")
    surfhrd = fields.Char("表面硬度")
    coreform = fields.Char("心部規格")
    corehrd = fields.Char("心部硬度")
    tensihrd = fields.Char("抗拉強度")
    commitstrenth = fields.Char("保證強度")

    elongation = fields.Float("伸長率")
    sectionshrink = fields.Float("斷面收縮")
    ystrength = fields.Float("降伏點強度")
    carburlayer = fields.Char("滲碳層")
    safeload = fields.Float("安全負荷")
    headshot = fields.Integer("頭部敲擊")
    innertensihrd = fields.Char("內部抗拉強度")
    innercarburlayer = fields.Char("內部滲碳層")
    innersurfhrd = fields.Char("內部表面硬度")
    innercorehrd = fields.Char("內部心部硬度")
    note = fields.Char("備註")


class YcTorsion(models.Model):
    _name = "yc.torsion"

    name = fields.Char("自動編號")

    clsf_code = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    torsion1 = fields.Float("扭力值1")
    torsion2 = fields.Float("扭力值2")

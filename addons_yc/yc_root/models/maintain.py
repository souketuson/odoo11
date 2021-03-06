# -*- coding: utf-8 -*-


from odoo import models, fields, api


# S01
# class YcSetFactory(models.Model):
#     # 廠別 S01N0001
#     _name = "yc.setfactory"
#     name = fields.Char("廠別名稱")
#     code = fields.Char("廠別代碼")
#     params1 = fields.Char("參數1")


class YcSetDepartment(models.Model):
    # 部門 S01N0002
    _name = 'yc.department'
    name = fields.Char(string='部門名稱')
    code = fields.Char(string='部門代碼')


class YcSetJobTitle(models.Model):
    # 職稱 S01N0004
    _name = "yc.setjobtitle"
    name = fields.Char("職稱")
    code = fields.Char("職稱代碼")


class YcSetSalaryItem(models.Model):
    # 薪資項目 S01N0005
    _name = "yc.setsalaryitem"
    name = fields.Char("薪資項目名稱")
    code = fields.Char("薪資項目代碼")


class YcSetshift(models.Model):
    # 班別 S01N0006
    _name = "yc.setshift"
    name = fields.Char("班別名稱")
    code = fields.Char("班別代碼")
    other1 = fields.Char("其他1")
    other2 = fields.Char("其他2")
    other3 = fields.Char("其他3")


class YcSetleave(models.Model):
    # 假別 S01N0007
    _name = "yc.setleave"
    name = fields.Char("假別名稱")
    code = fields.Char("假別代碼")


class YcSetBonus(models.Model):
    # 獎金 S01N0008
    _name = "yc.setbonus"

    name = fields.Char("獎金項目")
    code = fields.Char("獎金代碼")


# S02
class YcSetcustomertype(models.Model):
    # 客戶種類 S02N0001
    _name = "yc.setcustomertype"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


class YcSetsuppliertype(models.Model):
    # 廠商種類 S02N0002
    _name = "yc.setsuppliertype"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


class YcSetpayment(models.Model):
    # 付款方式 S02N0003
    _name = "yc.setpayment"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


class YcSetcurrency(models.Model):
    # 貨幣設定 S02N0004
    _name = "yc.setcurrency"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


class YcSetprocessingplanttype(models.Model):
    # 加工廠種類設定 S02N0005
    _name = "yc.setprocessingplanttype"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


class YcSetprocessingareatype(models.Model):
    # 加工廠區域設定 S02N0005
    _name = "yc.setprocessingareatype"
    name = fields.Char("名稱")
    code = fields.Char("代碼")


# S03
class YcSetproduct(models.Model):
    # 產品資料 S03N0001
    _name = "yc.setproduct"
    name = fields.Char("產品名稱")
    code = fields.Char("產品代碼")

    # @api.multi
    # def name_get(self):
    #     return [(record.id, "%s %s" % (record.code, record.name)) for record in self]

    # 讓many2one下拉可以搜尋"代碼"來找產品
    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = args or []
    #     if u'\u4e00' <= name <= u'\u9fff':
    #         domain = [('name', operator, name)]
    #     else:
    #         domain = ['|', ('code', operator, name), ('name', operator, name)]
    #     product = self.search(domain + args, limit=limit, order='name asc')
    #     return product.name_get()


class YcSetstrength(models.Model):
    # 強度級數 S04N0002
    _name = "yc.setstrength"
    name = fields.Char("強度名稱")
    code = fields.Char("強度代碼")

    # 讓many2one下拉可以搜尋"代碼"來找產品
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if (name[0:1].capitalize() == 'G' and name[1:2]) or (name[0:5].upper() == 'GRADE'):
            domain = [('name', operator,
                       "Grade %s" % name.upper().replace('G', '').replace('R', '').replace('A', '').replace('D',
                                                                                                            '').replace(
                           'E', '').replace(' ',''))]
        else:
            domain = [('name', operator, name)]
        product = self.search(domain + args, limit=limit, order='name asc')
        return product.name_get()


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
    parameter1 = fields.Char("參數1")
    parameter2 = fields.Char("參數2")
    parameter3 = fields.Char("參數3")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if name[0:1].capitalize() == 'M' and name[1:2]:
            domain = [('name', operator, "M%s" % name[1:4])]
        else:
            domain = [('name', operator, name)]
        norm = self.search(domain + args, limit=limit, order='name asc')
        return norm.name_get()


class YcSetlength(models.Model):
    # 長度 S03N0005
    _name = "yc.setlength"
    name = fields.Char("長度名稱")
    code = fields.Char("長度代碼")
    parameter1 = fields.Char("參數1")
    parameter2 = fields.Char("參數2")
    parameter3 = fields.Char("參數3")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = [('name', '=like', '{0}%'.format(name))]
        length = self.search(domain + args, limit=limit, order='name asc')
        return length.name_get()


class YcSetprocess(models.Model):
    #  加工方式 S03N0006
    _name = "yc.setprocess"
    name = fields.Char("加工方式")
    code = fields.Char("加工方式代碼")


class YcSettexture(models.Model):
    # 材質 S03N0007
    _name = "yc.settexture"
    _order = "name asc"
    name = fields.Char("材質名稱")
    code = fields.Char("材質代碼")

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = (id desc)
    #     return self.search(args, limit=limit).name_get()


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
    # 單位 S03N0010
    _name = "yc.setunit"
    name = fields.Char("單位名稱")
    code = fields.Char("單位代碼")


class YcSetPurchasenote(models.Model):
    # 製造備註 S03N0012
    _name = "yc.setpurchasenote"
    name = fields.Char()


class YcSetStatus(models.Model):
    # 狀態
    _name = "yc.setstatus"
    name = fields.Char("狀態")
    code = fields.Char("狀態代碼")


class YcSetfurnace(models.Model):
    # 爐號
    _name = "yc.setfurnace"
    name = fields.Char("爐號")
    code = fields.Char("代碼")


class YcFactory(models.Model):
    _name = "yc.factory"
    name = fields.Char("廠別名稱")
    code = fields.Char("廠別代碼")


class YcSetStoreplace(models.Model):
    _name = "yc.setstoreplace"
    name = fields.Char("存放地點")
    company_id = fields.Many2one("res.company", string='所屬工廠')


# S04
class YcSetproducenote(models.Model):
    # 品質管理-製造備註 S04N0001
    _name = "yc.setproducenote"
    name = fields.Char("備註名稱")
    code = fields.Char("備註代碼")
    parameter1 = fields.Char("參數1")
    parameter2 = fields.Char("參數2")
    parameter3 = fields.Char("參數3")


class YcSethardness(models.Model):
    # 品質管理-硬度 S04N0003
    _name = "yc.sethardness"
    name = fields.Char("硬度名稱")
    code = fields.Char("硬度代碼")
    parameter1 = fields.Char("參數1")
    parameter2 = fields.Char("參數2")
    parameter3 = fields.Char("參數3")


class YcSetqcnote(models.Model):
    # 品質管理-品管備註 S04N0004
    _name = "yc.setqcnote"
    name = fields.Char("備註名稱")
    code = fields.Char("備註代碼")
    parameter1 = fields.Char("參數1")
    parameter2 = fields.Char("參數2")
    parameter3 = fields.Char("參數3")


class YcSettorsion(models.Model):
    # 品質管理-扭力 S04N0005
    _name = "yc.settorsion"
    name = fields.Char()
    clsf_id = fields.Many2one("yc.setproductclassify", string="品名分類")
    strength_id = fields.Many2one("yc.setstrength", string="強度級數")
    norm_id = fields.Many2one("yc.setnorm", string="直徑規格")
    parameter1 = fields.Char("扭力值1")
    parameter2 = fields.Char("扭力值2")


class YcSetfulorhalf(models.Model):
    _name = 'yc.setfulorhalf'
    name = fields.Char(string='名稱')

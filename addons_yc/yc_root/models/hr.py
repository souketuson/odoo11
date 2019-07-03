# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime as dt


class YcHR(models.Model):
    _name = 'yc.hr'
    code = fields.Char(string="員工代號")
    password = fields.Char(string="密碼")
    factory_id = fields.Many2one("yc.factory", string="廠別")
    dep_id = fields.Many2one('yc.department', string="所屬部門")
    employee_type = fields.Char(string="僱用關係")
    job_title1 = fields.Char("職稱代碼1")
    job_title2 = fields.Char("職稱代碼2")
    job_title3 = fields.Char("職稱代碼3")
    name = fields.Char(string="員工姓名")
    gender = fields.Selection(
        [('M', '男性'), ('F', '女性'),
         ('O', '其他')], '性別')
    idcard = fields.Char(string="身分證號")
    birthday = fields.Date('出生日期')
    birthplace = fields.Char("籍貫")
    marrige = fields.Selection([("已婚", "已婚"), ("未婚", "未婚"), ("其他", "其他")], "婚姻")
    children = fields.Char("子女數")
    phone = fields.Char("電話")
    mobile = fields.Char("手機")
    email = fields.Char("E Mail")
    address1 = fields.Char("通訊地址")
    address2 = fields.Char("戶籍地址")
    nok = fields.Char("緊急聯絡人")
    relationship = fields.Char("關係")
    emergphone = fields.Char("聯絡電話")
    emergmobile = fields.Char("聯絡手機")
    duty_date = fields.Date("到職日")
    leave_date = fields.Date("離職日")
    note = fields.Text("備註")
    lastlogtime = fields.Char("最後登入時間")
    log_state = fields.Selection([("Y", "是"), ("N", "否")], "允許登入")

    pay = fields.Char("基本薪資")
    raise_no = fields.Char("扶養人數")
    txcredit_date = fields.Date("代扣所得税日期")
    txcredit = fields.Char("代扣所得稅")
    labor_insured_date = fields.Date("勞保加保日期")
    labor_insured_income = fields.Char("勞保投保薪資")
    labor_insured_charge = fields.Char("勞保保費")
    health_insured_date = fields.Date("健保投保日期")
    health_insured_income = fields.Char("健保投保薪資")
    health_insured_charge = fields.Char("健保保費")
    ac_post = fields.Char("立帳郵局")
    post_no = fields.Char("郵局局號")
    post_ac = fields.Char("郵局帳號")
    ac_name = fields.Char("戶名")
    seniority = fields.Char(string="年資", compute="_get_year", store=True)

    # 特休日數
    # annual_leave_total
    # 已休日數
    # annual_leave_take
    # 剩餘特休
    # annual_leave_last

    @api.depends("duty_date", "leave_date")
    def _get_year(self):

        '''用@api.depemds decorator 隨時更新數值
        判斷離職或非離職，用datetime模組
        strptime 和 strftime方法格式化日期

        問題：如果非透過網頁創建資料 而是直接在postgre匯入資料 資料庫不會自動計算年資
        一定要經過邏輯層
        '''
        if self.duty_date == False:
            pass
        else:
            duty_date = dt.strptime(self.duty_date, "%Y-%m-%d")
            now = dt.now().strftime("%Y-%m-%d")
            form_now = dt.strptime(now, "%Y-%m-%d")

            if self.leave_date and self.leave_date != '':
                delta = dt.strptime(self.leave_date, "%Y-%m-%d") - duty_date
            else:
                delta = form_now - duty_date

            self.seniority = int(delta.days / 365)


class YcDriver(models.Model):
    _name = "yc.driver"

    name = fields.Char("姓名")
    code = fields.Char("司機代號")
    category = fields.Char("分類")
    user_code = fields.Char("員工代號")
    plate_no = fields.Char("車牌號碼")
    gender = fields.Selection(
        [('M', '男性'), ('F', '女性'),
         ('O', '其他')], '性別')
    idcard = fields.Char(string="身分證號")
    birthday = fields.Date("出生日期")
    birthplace = fields.Char("籍貫")
    phone = fields.Char("電話")
    mobile = fields.Char("手機")
    address2 = fields.Char("戶籍地址")
    address1 = fields.Char("通訊")
    refine_price = fields.Char("調質單價")
    carburize_price = fields.Char("滲碳單價")
    note = fields.Text("備註")

    def _fetch(self):
        # fetch create_date and write_date in database
        self.add_date = self.create_date
        self.edit_date = self.write_date


class User(models.Model):
    _inherit = 'res.users'

    factory_id = fields.Many2one("yc.factory", string="廠別")


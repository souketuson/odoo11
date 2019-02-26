# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime


class Human_resource(models.Model):
    _name = 'hr.main'

    name = fields.Char(string="員工姓名", required=True)
    code = fields.Char(string="員工代號")

    factory_id = fields.Char(string="廠別")
    employee_type = fields.Char(string="僱用關係")
    dep_id = fields.Many2one('yc.department', string="所屬部門")
    idcard = fields.Char(string="身分證號")
    birth_date = fields.Date('出生日期')
    gender = fields.Selection(
        [('m', '男性'), ('f', '女性'),
         ('o', '其他')], '性別')
    description = fields.Text()

    # 密碼
    # password

    job_title1 = fields.Char("職稱代碼1")
    job_title2 = fields.Char("職稱代碼2")
    job_title3 = fields.Char("職稱代碼3")
    birthplace = fields.Char("籍貫")
    marrige = fields.Selection([("m", "已婚"), ("s", "未婚"), ("o", "其他")], "婚姻")
    children = fields.Char("子女數")
    phone1 = fields.Char("電話")
    phone2 = fields.Char("手機")
    email = fields.Char("E Mail")
    address1 = fields.Char("通訊地址")
    address2 = fields.Char("戶籍地址")
    nok = fields.Char("緊急聯絡人")
    relationship = fields.Char("關係")
    emergency_phone1 = fields.Char("聯絡電話")
    emergency_phone2 = fields.Char("聯絡手機")
    duty_date = fields.Date("到職日")
    leave_date = fields.Date("離職日")
    note = fields.Text("備註")

    # 最後登入時間
    # last_login_time
    log_state = fields.Selection([("y", "是"), ("n", "否")], "允許登入")

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
    seniority = fields.Char(string="年資", compute="_get_year")

    # 特休日數
    # annual_leave_total
    # 已休日數
    # annual_leave_take
    # 剩餘特休
    # annual_leave_last

    @api.depends("duty_date", "leave_date")
    def _get_year(self):
        """
        用@api.depemds decorator 隨時更新數值
        判斷離職或非離職，用datetime模組
        strptime 和 strftime方法格式化日期
        :return: 年資
        """
        duty_date = datetime.strptime(self.duty_date, "%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d")
        form_now = datetime.strptime(now, "%Y-%m-%d")

        if self.leave_date:
            delta = datetime.strptime(self.leave_date, "%Y-%m-%d") - duty_date
        else:
            delta = form_now - duty_date

        self.seniority = int(delta.days / 365)


class Driver(models.Model):
    _name = "driver.main"

    name = fields.Char("司機姓名", required=True)
    driver_code = fields.Char("司機代號")
    category = fields.Char("分類")
    user_code = fields.Char("員工代號")
    plate_no = fields.Char("車牌號碼")
    gender = fields.Selection(
        [('m', '男性'), ('f', '女性'),
         ('o', '其他')], '性別')
    idcard = fields.Char(string="身分證號")
    birth_date = fields.Date("出生日期")
    birthplace = fields.Char("籍貫")
    phone1 = fields.Char("電話")
    phone2 = fields.Char("手機")
    address2 = fields.Char("戶籍地址")
    address1 = fields.Char("通訊")
    refine_price = fields.Char("調質單價")
    carburize_price = fields.Char("滲碳單價")
    note = fields.Text("備註")
    adder = fields.Many2one("hr.main", "建立人員")
    add_date = fields.Date("建立日期", compute="_fetch")
    editor = fields.Many2one("hr.main", "修改人員")
    edit_date = fields.Date("修改日期", compute="_fetch")

    def _fetch(self):
        # fetch create_date and write_date in database
        self.add_date = self.create_date
        self.edit_date = self.write_date


class Department(models.Model):
    _name = 'yc.department'
    name = fields.Char(string='部門名稱', required=True)
    code = fields.Char(string='部門代碼')


class Factory(models.Model):
    _name = "yc.factory"

    name = fields.Char("廠別名稱")
    code = fields.Char("廠別代碼")


class Job_title(models.Model):
    _name = "yc.job_title"

    name = "職稱"
    code = "職稱代碼"


class Salary_item(models.Model):
    _name = "yc.salary.item"

    name = "薪資項目名稱"
    code = "薪資項目代碼"


class Shift(models.Model):
    _name = "yc.shift"

    name = fields.Char("班制選項")
    code = fields.Char("代碼")

    on_duty = fields.Char("上班時間")
    off_duty = fields.Char("下班時間")


class Leave(models.Model):
    _name = "yc.leave"

    name = fields.Char("假別選項")
    code = fields.Char("假別代碼")


class Bonus(models.Model):
    _name = "yc.bonus"

    name = fields.Char("獎金項目")
    code = fields.Char("獎金代碼")

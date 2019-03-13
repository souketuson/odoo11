from odoo import models, fields, api

class Salary(models.Model):
    _name = "hr.salary"


    pay_code = fields.Char(string='薪資代碼')
    # 一個薪資代碼 對應多個員工
    pay = fields.Char(string='基本薪資')
    # 扶養人數

    raise_no = fields.Char(string='扶養人數')

    # 代扣所得稅年月
    # help_income_txcredit_date
    # 代扣所得稅
    # help_income_txcredit
    # 勞保投保日期
    # labor_Insured_date
    # 勞保投保薪資
    # labor_Insured_income
    # 勞保保費
    # labor_Insured_charge
    # 健保投保日期
    # health_insured_date
    # 健保投保薪資
    # health_insured_income
    # 健保保費
    # health_insured_charge
    # 立帳郵局
    # account_post
    # 郵局局號
    # post_no
    # 郵局帳號
    # post_account
    # 戶名
    # account_name
    # 戶名身份證號
    # 和員工身分證號idcard_no
    # 一樣?
    # 年資
    # seniority
    # 特休日數
    # annual_leave_total
    # 已休日數
    # annual_leave_take
    # 剩餘特休
    # annual_leave_last


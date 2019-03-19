# -*- coding: utf-8 -*-

import logging
import pyodbc

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    _description = u"App Odoo Customize settings"
    app_system_name = fields.Char('System Name', help=u"Setup System Name,which replace Odoo")
    app_show_lang = fields.Boolean('Show Quick Language Switcher',
                                   help=u"When enable,User can quick switch language in user menu")
    app_show_debug = fields.Boolean('Show Quick Debug', help=u"When enable,everyone login can see the debug menu")
    app_show_documentation = fields.Boolean('Show Documentation', help=u"When enable,User can visit user manual")
    app_show_documentation_dev = fields.Boolean('Show Developer Documentation',
                                                help=u"When enable,User can visit development documentation")
    app_show_support = fields.Boolean('Show Support', help=u"When enable,User can vist your support site")
    app_show_account = fields.Boolean('Show My Account', help=u"When enable,User can login to your website")
    app_show_enterprise = fields.Boolean('Show Enterprise Tag', help=u"Uncheck to hide the Enterprise tag")
    app_show_share = fields.Boolean('Show Share Dashboard', help=u"Uncheck to hide the Odoo Share Dashboard")
    app_show_poweredby = fields.Boolean('Show Powered by Odoo', help=u"Uncheck to hide the Powered by text")
    app_stop_subscribe = fields.Boolean('Stop Odoo Subscribe(Performance Improve)',
                                        help=u"Check to stop Odoo Subscribe function")
    group_show_author_in_apps = fields.Boolean(string="Show Author in Apps Dashboard",
                                               implied_group='app_odoo_customize.group_show_author_in_apps',
                                               help=u"Uncheck to Hide Author and Website in Apps Dashboard")
    group_show_quick_upgrade = fields.Boolean(string="Show Quick Upgrade in Apps Dashboard",
                                              implied_group='app_odoo_customize.group_show_quick_upgrade',
                                              help=u"Uncheck to show normal install in Apps Dashboard")

    app_documentation_url = fields.Char('Documentation Url')
    app_documentation_dev_url = fields.Char('Developer Documentation Url')
    app_support_url = fields.Char('Support Url')
    app_account_title = fields.Char('My Odoo.com Account Title')
    app_account_url = fields.Char('My Odoo.com Account Url')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_system_name = ir_config.get_param('app_system_name', default='odooApp')

        app_show_lang = True if ir_config.get_param('app_show_lang') == "True" else False
        app_show_debug = True if ir_config.get_param('app_show_debug') == "True" else False
        app_show_documentation = True if ir_config.get_param('app_show_documentation') == "True" else False
        app_show_documentation_dev = True if ir_config.get_param('app_show_documentation_dev') == "True" else False
        app_show_support = True if ir_config.get_param('app_show_support') == "True" else False
        app_show_account = True if ir_config.get_param('app_show_account') == "True" else False
        app_show_enterprise = True if ir_config.get_param('app_show_enterprise') == "True" else False
        app_show_share = True if ir_config.get_param('app_show_share') == "True" else False
        app_show_poweredby = True if ir_config.get_param('app_show_poweredby') == "True" else False
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe') == "True" else False

        app_documentation_url = ir_config.get_param('app_documentation_url',
                                                    default='http://www.sunpop.cn/documentation/user/10.0/en/index.html')
        app_documentation_dev_url = ir_config.get_param('app_documentation_dev_url',
                                                        default='http://www.sunpop.cn/documentation/10.0/index.html')
        app_support_url = ir_config.get_param('app_support_url', default='http://www.sunpop.cn/trial/')
        app_account_title = ir_config.get_param('app_account_title', default='My Online Account')
        app_account_url = ir_config.get_param('app_account_url', default='http://www.sunpop.cn/my-account/')
        res.update(
            app_system_name=app_system_name,
            app_show_lang=app_show_lang,
            app_show_debug=app_show_debug,
            app_show_documentation=app_show_documentation,
            app_show_documentation_dev=app_show_documentation_dev,
            app_show_support=app_show_support,
            app_show_account=app_show_account,
            app_show_enterprise=app_show_enterprise,
            app_show_share=app_show_share,
            app_show_poweredby=app_show_poweredby,
            app_stop_subscribe=app_stop_subscribe,

            app_documentation_url=app_documentation_url,
            app_documentation_dev_url=app_documentation_dev_url,
            app_support_url=app_support_url,
            app_account_title=app_account_title,
            app_account_url=app_account_url
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter']
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_show_lang", self.app_show_lang or "False")
        ir_config.set_param("app_show_debug", self.app_show_debug or "False")
        ir_config.set_param("app_show_documentation", self.app_show_documentation or "False")
        ir_config.set_param("app_show_documentation_dev", self.app_show_documentation_dev or "False")
        ir_config.set_param("app_show_support", self.app_show_support or "False")
        ir_config.set_param("app_show_account", self.app_show_account or "False")
        ir_config.set_param("app_show_enterprise", self.app_show_enterprise or "False")
        ir_config.set_param("app_show_share", self.app_show_share or "False")
        ir_config.set_param("app_show_poweredby", self.app_show_poweredby or "False")
        ir_config.set_param("app_stop_subscribe", self.app_stop_subscribe or "False")

        ir_config.set_param("app_documentation_url",
                            self.app_documentation_url or "http://www.sunpop.cn/documentation/user/10.0/en/index.html")
        ir_config.set_param("app_documentation_dev_url",
                            self.app_documentation_dev_url or "http://www.sunpop.cn/documentation/10.0/index.html")
        ir_config.set_param("app_support_url", self.app_support_url or "http://www.sunpop.cn/trial/")
        ir_config.set_param("app_account_title", self.app_account_title or "My Online Account")
        ir_config.set_param("app_account_url", self.app_account_url or "http://www.sunpop.cn/my-account/")

    @api.multi
    def remove_sales(self):
        to_removes = [
            # 清除销售单据
            ['sale.order.line', ],
            ['sale.order', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'sale.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='sale.order';"
            self._cr.execute(sql)
        except Exception as e:
            raise Warning(e)
        return True

    def remove_product(self):
        to_removes = [
            # 清除产品数据
            ['product.product', ],
            ['product.template', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号,针对自动产品编号
            seqs = self.env['ir.sequence'].search([('code', '=', 'product.product')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='product.product';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    def remove_product_attribute(self):
        to_removes = [
            # 清除产品属性
            ['product.attribute.value', ],
            ['product.attribute', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_pos(self):
        to_removes = [
            # 清除POS单据
            ['pos.order.line', ],
            ['pos.order', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'pos.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='pos.order';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_purchase(self):
        to_removes = [
            # 清除采购单据
            ['purchase.order.line', ],
            ['purchase.order', ],
            ['purchase.requisition.line', ],
            ['purchase.requisition', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'purchase.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='purchase.order';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_mrp(self):
        to_removes = [
            # 清除生产单据
            ['mrp.workcenter.productivity', ],
            ['mrp.workorder', ],
            ['mrp.production.workcenter.line', ],
            ['change.production.qty', ],
            ['mrp.production', ],
            ['mrp.production.product.line', ],
            ['mrp.unbuild', ],
            ['change.production.qty', ],
            ['sale.forecast.indirect', ],
            ['sale.forecast', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search(['|', ('code', '=', 'mrp.production'), ('code', '=', 'mrp.unbuild')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (code ='mrp.production' or code ='mrp.unbuild');"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_mrp_bom(self):
        to_removes = [
            # 清除生产BOM
            ['mrp.bom.line', ],
            ['mrp.bom', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_inventory(self):
        to_removes = [
            # 清除库存单据
            ['stock.quant', ],
            ['stock.quant.package', ],
            ['stock.quant.move.rel', ],
            ['stock.move.line', ],
            ['stock.move', ],
            ['stock.pack.operation', ],
            ['stock.picking', ],
            ['stock.scrap', ],
            ['stock.inventory.line', ],
            ['stock.inventory', ],
            ['stock.production.lot', ],
            ['stock.fixed.putaway.strat', ],
            ['make.procurement', ],
            ['procurement.order', ],
            ['procurement.group', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'stock.lot.serial'),
                '|', ('code', '=', 'stock.lot.tracking'),
                '|', ('code', '=', 'stock.orderpoint'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('code', '=', 'stock.quant.package'),
                '|', ('code', '=', 'stock.scrap'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('prefix', '=', 'WH/IN/'),
                '|', ('prefix', '=', 'WH/INT/'),
                '|', ('prefix', '=', 'WH/OUT/'),
                '|', ('prefix', '=', 'WH/PACK/'),
                ('prefix', '=', 'WH/PICK/')
            ])

            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (" \
                  "code ='stock.lot.serial' " \
                  "or code ='stock.lot.tracking' " \
                  "or code ='stock.orderpoint'" \
                  "or code ='stock.picking'" \
                  "or code ='stock.quant.package'" \
                  "or code ='stock.scrap'" \
                  "or code ='stock.picking'" \
                  "or prefix ='WH/IN/'" \
                  "or prefix ='WH/INT/'" \
                  "or prefix ='WH/OUT/'" \
                  "or prefix ='WH/PACK/'" \
                  "or prefix ='WH/PICK/'" \
                  ");"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_account(self):
        to_removes = [
            # 清除财务会计单据
            ['account.voucher.line', ],
            ['account.voucher', ],
            ['account.bank.statement.line', ],
            ['account.bank.statement', ],
            ['account.payment', ],
            ['account.analytic.line', ],
            ['account.analytic.account', ],
            ['account.invoice.line', ],
            ['account.invoice.refund', ],
            ['account.invoice', ],
            ['account.partial.reconcile', ],
            ['account.move.line', ],
            ['hr.expense.sheet', ],
            ['account.move', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

                    # 更新序号
                    seqs = self.env['ir.sequence'].search([
                        '|', ('code', '=', 'account.reconcile'),
                        '|', ('code', '=', 'account.payment.customer.invoice'),
                        '|', ('code', '=', 'account.payment.customer.refund'),
                        '|', ('code', '=', 'account.payment.supplier.invoice'),
                        '|', ('code', '=', 'account.payment.supplier.refund'),
                        '|', ('code', '=', 'account.payment.transfer'),
                        '|', ('prefix', 'like', 'BNK1/'),
                        '|', ('prefix', 'like', 'CSH1/'),
                        '|', ('prefix', 'like', 'INV/'),
                        '|', ('prefix', 'like', 'EXCH/'),
                        '|', ('prefix', 'like', 'MISC/'),
                        '|', ('prefix', 'like', u'账单/'),
                        ('prefix', 'like', u'杂项/')
                    ])

                    for seq in seqs:
                        seq.write({
                            'number_next': 1,
                        })
                    # todo: 帐单 or BILL/%
                    sql = "update ir_sequence set number_next=1 where (" \
                          "code ='account.reconcile' " \
                          "or code ='account.payment.customer.invoice' " \
                          "or code ='account.payment.customer.refund' " \
                          "or code ='account.payment.supplier.invoice' " \
                          "or code ='account.payment.supplier.refund' " \
                          "or prefix like 'BNK1/%'" \
                          "or prefix like 'CSH1/%'" \
                          "or prefix like 'INV/%'" \
                          "or prefix like 'EXCH/%'" \
                          "or prefix like 'MISC/%'" \
                          "or prefix like '账单/%'" \
                          "or prefix like '杂项/%'" \
                          ");"
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_account_chart(self):
        to_removes = [
            # 清除财务科目，用于重设
            ['account.tax.account.tag', ],
            ['account.tax', ],
            ['account.account.account.tag', ],
            ['wizard_multi_charts_accounts'],
            ['account.account', ],
            ['account.journal', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

            # reset default tax，不管多公司
            field1 = self.env['ir.model.fields']._get('product.template', "taxes_id").id
            field2 = self.env['ir.model.fields']._get('product.template', "supplier_taxes_id").id

            sql = ("delete from ir_default where field_id = %s or field_id = %s") % (field1, field2)
            self._cr.execute(sql)

            sql = "update res_company set chart_template_id=null ;"
            self._cr.execute(sql)
            # 更新序号
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_project(self):
        to_removes = [
            # 清除项目
            ['account.analytic.line', ],
            ['project.task', ],
            ['project.forecast', ],
            ['project.project', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_message(self):
        to_removes = [
            # 清除消息数据
            ['mail.message', ],
            ['mail.followers', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_workflow(self):
        to_removes = [
            # 清除工作流
            ['wkf.workitem', ],
            ['wkf.instance', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

        except Exception as e:
            pass
        return True

    @api.multi
    def remove_all_biz(self):
        try:
            self.remove_account()
            self.remove_inventory()
            self.remove_mrp()
            self.remove_purchase()
            self.remove_sales()
            self.remove_project()
            self.remove_message()
        except Exception as e:
            pass
        return True

    # 以下進舊資料庫拉資料到pgsql
    # 員工主檔轉資料庫 ERPALL > pgsql
    @api.multi
    def insert_yc_hr(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 員工主檔")
            rows = cursor.fetchall()
            hr = self.env["yc.hr"].search([])

            sql = "delete from yc_hr"
            self._cr.execute(sql)

            for row in rows:
                factory_id_check = self.env["yc.factory"].search([("code", '=', row.廠別代碼)])
                dep_id_check = self.env["yc.department"].search([("code", '=', row.部門代碼)])
                hr.create({
                    "code": row.員工代號, "password": row.密碼,
                    "factory_id": factory_id_check.id, "dep_id": dep_id_check.id,
                    "employee_type": row.僱用性質代碼, "job_title1": row.職稱代碼1,
                    "job_title2": row.職稱代碼2, "job_title3": row.職稱代碼3,
                    "name": row.姓名, "gender": row.性別,
                    "idcard": row.身份證號, "birthday": row.出生日期,
                    "birthplace": row.籍貫, "marrige": row.婚姻,
                    "children": row.子女數, "phone": row.電話,
                    "mobile": row.手機, "email": row.E_Mail,
                    "address1": row.通訊地址, "address2": row.戶籍地址,
                    "nok": row.緊急聯絡人, "relationship": row.關係,
                    "emergphone": row.聯絡電話, "emergmobile": row.聯絡手機,
                    "duty_date": row.到職日期, "leave_date": row.離職日期,
                    "note": row.備註, "lastlogtime": row.最後登入時間,
                    "log_state": row.登入否,
                })

        except Exception as e:
            pass
        return True

    # 司機主檔轉資料庫 ERPALL > pgsql
    @api.multi
    def insert_yc_driver(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 司機主檔")
            rows = cursor.fetchall()
            driver = self.env["yc.driver"].search([])
            sql = "delete from yc_driver"
            self._cr.execute(sql)

            for row in rows:
                # 先去除空白
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].replace(' ', '')

                driver.create({
                    "code": row.司機代號, "category": row.分類,
                    "user_code": row.員工代號, "plate_no": row.車牌號碼,
                    "name": row.姓名, "gender": row.性別,
                    "birthday": row.出生日期, "birthplace": row.籍貫,
                    "phone": row.電話, "mobile": row.手機,
                    "address2": row.戶籍地址, "address1": row.通訊地址,
                    "refine_price": row.調質單價, "carburize_price": row.滲碳單價,
                    "note": row.備註,
                })

        except Exception as e:
            pass
        return True

    # 過磅單主檔
    @api.multi
    def insert_weight_main(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 過磅單主檔")
            rows = cursor.fetchmany(500)
            weight = self.env["yc.weight"].search([])
            sql = "delete from yc_weight"
            self._cr.execute(sql)

            for row in rows:
                # 先去除空白
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].replace(' ', '')

                driver_id = self.env["yc.driver"].search([("code", '=', row.司機代號)])
                person_id = self.env["yc.hr"].search([("code", '=', row.過磅人員)])
                factory_id = self.env["yc.factory"].search([("name", '=', row.所屬工廠)])
                if row.司機代號:
                    weight.create({
                        "name": row.過磅單號, "in_out": row.分類,
                        "driver_id": driver_id.id, "day": row.日期,
                        "weightime": row.時間, "carno": row.車次序號,
                        "person_id": person_id.id, "weighbridge": row.地磅序號,
                        "plate_no": row.車號, "refine": row.調質重量,
                        "total": row.總重, "carbur": row.滲碳重量,
                        "curbweight": row.空車重, "other": row.其他重量,
                        "emptybucket": row.空桶重, "net": row.淨重,
                        "purchase_times": row.進貨次數, "ship_times": row.出貨次數,
                        "note": row.備註, "other1": row.其他重量1,
                        "factory_id": factory_id.id,
                    })
        except Exception as e:
            pass
        return True

    # 過磅單項目檔 處理完主檔才能處理項目檔
    @api.multi
    def insert_weight_details(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            weight = self.env["yc.weight"].search([]).name_get()
            _string = ''
            for x in range(len(weight)):
                if x != len(weight) - 1:
                    _string += "'" + weight[x][1] + "',"
                else:
                    _string += "'" + weight[x][1] + "'"
            # SQL strict form: SELECT * FROM 過磅單項目檔 WHERE 過磅單號 IN('xxxxxxxxx','oooooo')
            db_sql = "SELECT * FROM 過磅單項目檔 WHERE 過磅單號 IN(%s)" % _string
            cursor.execute(db_sql)

            rows = cursor.fetchall()
            weight_item = self.env["yc.weight.details"].search([])
            sql = "delete from yc_weight_details"
            self._cr.execute(sql)

            for row in rows:
                # 防止 ValueError
                if row.客戶代號 != None:
                    row.客戶代號 = row.客戶代號.strip("\x00")
                if row.加工廠代號 != None:
                    row.加工廠代號 = row.加工廠代號.strip("\x00")
                customer_id = self.env["yc.customer"].search([("code", '=', row.客戶代號)])
                processing_id = self.env["yc.processing"].search([("code", '=', row.加工廠代號)])
                name_id = self.env["yc.weight"].search([("name", "=", row.過磅單號)])

                weight_item.create({
                    "name": name_id.id,
                    "no": row.序號,
                    "customer_id": customer_id.id,
                    "processing_id": processing_id.id,
                    "note": row.備註,
                })
        except Exception as e:
            pass
        return True

    # 過磅單主檔 & 項目檔合併 一鍵完成
    @api.multi
    def insert_yc_weight(self):
        insert_weight_main = ResConfigSettings.insert_weight_main
        insert_weight_details = ResConfigSettings.insert_weight_details
        funcs = insert_weight_main, insert_weight_details
        for func in funcs:
            func(self)

    @api.multi
    def insert_processing(self):
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM 加工廠主檔")
        rows = cursor.fetchall()
        processing = self.env["yc.processing"].search([])
        sql = "delete from yc_processing"
        self._cr.execute(sql)

        for row in rows:
            processing.create({
                "name": row.公司名稱,
                "code": row.加工廠代號,
            })

    @api.multi
    def insert_customer(self):
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM 客戶主檔")
        rows = cursor.fetchall()
        customer = self.env["yc.customer"].search([])
        sql = "delete from yc_customer"
        self._cr.execute(sql)

        for row in rows:
            customer.create({
                "name": row.公司名稱,
                "code": row.客戶代號,
            })

# class DataBaseConnection(models.Model):
#     def __init__(self, origin_db, to_db, d_sql, kwarg):
#         '''
#         :param origin_db: 來源資料庫
#         :param to_db:  目標資料庫
#         :param d_sql: 清空目標資料庫
#         :param kwarg: 新增欄位
#         '''
#         cnxn = pyodbc.connect(
#             'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
#         cursor = cnxn.cursor()
#         cursor.execute("SELECT * FROM %s") % origin_db
#         rows = cursor.fetchall()
#         db = self.env["%s"].search([]) % to_db
#         self.d_sql = d_sql
#
#     def _delete(self):
#         sql = "delete from %s" % self.d_sql
#         self._cr.execute(sql)

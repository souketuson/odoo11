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
    #         for row in rows:
    #             for key,val in kwarg:
    #                 db.create({kwarg[key]:row[val]})
    #
    #     def _delete(self):
    #         sql = "delete from %s" % self.d_sql
    #         self._cr.execute(sql)

    def insert_yc_mechanicalproperty(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 產品機械性質主檔")
            rows = cursor.fetchall()
            mp = self.env["yc.mechanicalproperty"].search([])
            sql = "delete from yc_mechanicalproperty"
            self._cr.execute(sql)
            for row in rows:
                # 先去除空白
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].rstrip(' ')
                product_cls = self.env["yc.setproductclassify"].search([('name', '=', row.產品分類代號)])
                strength_lv = self.env["yc.setstrength"].search([('name', '=', row.強度級數)])
                mp.create({
                    "name": row.自動編號,
                    "standard": row.依據標準,
                    "clsf_code": product_cls.id,
                    "stdcodeinit": row.規格代碼起,
                    "stdcodeend": row.規格代碼迄,
                    "stdreviewinit": row.規格對照起,
                    "stdreviewend": row.規格對照迄,
                    "strength_level": strength_lv.id,
                    "surfaceform": row.表面規格,
                    "surfhrd": row.表面硬度,
                    "coreform": row.心部規格,
                    "corehrd": row.心部硬度,
                    "tensihrd": row.抗拉強度,
                    "commitstrenth": row.保證強度,
                    "elongation": row.伸長率,
                    "sectionshrink": row.斷面收縮,
                    "ystrength": row.降伏點強度,
                    "carburlayer": row.滲碳層,
                    "safeload": row.安全負荷,
                    "headshot": row.頭部敲擊,
                    "innertensihrd": row.內部抗拉強度,
                    "innercarburlayer": row.內部滲碳層,
                    "innersurfhrd": row.內部表面硬度,
                    "innercorehrd": row.內部心部硬度,
                    "note": row.備註,
                })
        except Exception as e:
            pass
        return True

    def insert_yc_torsion(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 扭力規格主檔")
            rows = cursor.fetchall()
            torsion = self.env["yc.torsion"].search([])
            sql = "delete from yc_torsion"
            self._cr.execute(sql)
            for row in rows:
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].rstrip(' ')
                clsf = self.env["yc.setproductclassify"].search([("name", "=", row.品名分類)])
                strength = self.env["yc.setstrength"].search([("name", "=", row.強度級數)])
                norm = self.env["yc.setnorm"].search([("name", "=", row.直徑規格)])

                torsion.create({
                    "name": row.自動編號,
                    "clsf_code": clsf.id,
                    "strength_level": strength.id,
                    "norm_code": norm.id,
                    "torsion1": row.扭力值1,
                    "torsion2": row.扭力值2,
                })
        except Exception as e:
            pass
        return True

    def insert_purchase(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 進貨單主檔")
            rows = cursor.fetchmany(500)
            purchase = self.env["yc.purchase"].search([])
            sql = "delete from yc_purchase"
            self._cr.execute(sql)

            for row in rows:
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].rstrip(' ')
                        row[x] = row[x].lstrip(' ')

                driver = self.env["yc.driver"].search([("code", "=", row.司機代號)])
                processing = self.env["yc.processing"].search([("code", "=", row.所屬工廠)])
                factory = self.env["yc.factory"].search([("code", "=", row.加工廠代號)])
                # 丟車次序號
                carno = self.env["yc.weight"].search([("carno", "=", row.車次序號)])
                customer = self.env["yc.customer"].search([("code", "=", row.客戶代號)])
                employee = self.env["yc.hr"].search([("code", "=", row.開單人員)])
                clsf = self.env["yc.setproductclassify"].search([("name", "=", row.品名分類代碼)])
                strength = self.env["yc.setstrength"].search([("name", "=", row.強度級數)])
                norm = self.env["yc.setnorm"].search([("name", "=", row.規格代碼)])
                product = self.env["yc.setproduct"].search([("code", "=", row.產品代碼)])
                texture = self.env["yc.settexture"].search([("name", "=", row.材質代碼)])
                length = self.env["yc.setlength"].search([("name", "=", row.長度代碼)])
                process = self.env["yc.setprocess"].search([("name", "=", row.加工方式代碼)])
                surface = self.env["yc.setsurface"].search([("name", "=", row.表面處理代碼)])
                elecplate = self.env["yc.setelectroplating"].search([("name", "=", row.電鍍別代碼)])
                unit1 = self.env["yc.setunit"].search([("name", "=", row.單位代號1)])
                unit2 = self.env["yc.setunit"].search([("name", "=", row.單位代號2)])
                unit3 = self.env["yc.setunit"].search([("name", "=", row.單位代號3)])
                unit4 = self.env["yc.setunit"].search([("name", "=", row.單位代號4)])
                process1 = self.env["yc.processing"].search([("code", "=", row.次加工廠代號1)])
                process2 = self.env["yc.processing"].search([("code", "=", row.次加工廠代號2)])
                control = self.env["yc.hr"].search([("code", "=", row.操作人員)])
                qc = self.env["yc.hr"].search([("code", "=", row.品管人員)])
                shift = self.env["yc.setshift"].search([("name", "=", row.班別)])
                shift1 = self.env["yc.setshift"].search([("name", "=", row.班別1)])
                shift2 = self.env["yc.setshift"].search([("name", "=", row.班別2)])
                shift3 = self.env["yc.setshift"].search([("name", "=", row.班別3)])
                op1 = self.env["yc.hr"].search([("code", "=", row.操作人員1)])
                op2 = self.env["yc.hr"].search([("code", "=", row.操作人員2)])
                op3 = self.env["yc.hr"].search([("code", "=", row.操作人員3)])
                tm1 = self.env["yc.hr"].search([("code", "=", row.組長1)])
                tm2 = self.env["yc.hr"].search([("code", "=", row.組長2)])
                tm3 = self.env["yc.hr"].search([("code", "=", row.組長3)])
                p_op = self.env["yc.hr"].search([("code", "=", row.產量操作人員)])
                p_weight = self.env["yc.hr"].search([("code", "=", row.產量過磅人員)])
                productname = self.env["yc.setproduct"].search([("name", "=", row.產品名稱)])
                mgreviewer = self.env["yc.hr"].search([("code", "=", row.金相審核人員)])
                mgchecker = self.env["yc.hr"].search([("code", "=", row.金相檢驗人員)])
                ck_person = self.env["yc.hr"].search([("code", "=", row.檢驗人員)])

                purchase.create({
                    "name": row.工令號碼,
                    "day": row.進貨日期,
                    "time": row.時間,
                    "state": row.狀態,
                    "weighstate": row.過磅狀態,
                    "checkstate": row.檢驗狀態,
                    "driver_id": driver.id,
                    "factory_id": factory.id,
                    "processing_attache": processing.id,
                    "pre_order": row.前工令號碼,
                    # 這個要丟單號還是車次號碼?
                    "car_no": carno.name,
                    "customer_id": customer.id,
                    "batch": row.客戶批號,
                    # 還沒做客戶單號主檔
                    "customer_no": row.客戶單號,
                    "person": employee.id,
                    "clsf_code": clsf.id,
                    "strength_level": strength.id,
                    "norm_code": norm.id,
                    "product_code": product.id,
                    "txtur_code": texture.id,

                    "len_code": length.id,



                    "len_descript": row.長度說明,
                    "proces_code": process.id,
                    "surface_code": surface.id,
                    "elecpl_code": elecplate.id,
                    "portage": row.運費種類,

                    "num1": row.數量1,
                    "unit1": unit1.id,
                    "num2": row.數量2,
                    "unit2": unit2.id,
                    "num3": row.數量3,
                    "unit3": unit3.id,
                    "num4": row.數量4,
                    "unit4": unit4.id,
                    "storeplace": row.存放位置,
                    "net": row.淨重,
                    "process1": process1.id,
                    "process2": process2.id,
                    "totalpack": row.裝袋合計,
                    "standard": row.依據標準,
                    "wire_furn": row.線材爐號,
                    # 頭部記號要怎麼轉?
                    "surfhrd": row.表面硬度,
                    "corehrd": row.心部硬度,
                    "piece": row.試片,
                    "tensihrd": row.抗拉強度,
                    "carburlayer": row.滲碳層,
                    "torsion": row.扭力,
                    "retempt": row.回火溫度,
                    "pre_furn": row.以前爐號,
                    "order_furn": row.預排爐號,
                    "norcls": row.規範分類,
                    "wxr_txtur": row.華司材質,
                    "wxrhard": row.華司硬度,
                    "fullorhalf": row.牙分類,
                    "notices1": row.注意事項1,
                    "notices2": row.注意事項2,
                    "notices3": row.注意事項3,
                    "notices4": row.注意事項4,
                    "qcnote1": row.品管備註1,
                    "qcnote2": row.品管備註2,
                    "qcnote3": row.品管備註3,
                    "prodnote1": row.製造備註1,
                    "prodnote2": row.製造備註2,
                    "prodnote3": row.製造備註3,
                    "flow": row.流量,
                    "cp": row.CP值,
                    "nh31": row.氨值1,
                    "nh32": row.氨值2,
                    "nh33": row.氨值3,
                    "nh34": row.氨值4,
                    "heat1": row.加熱爐1,
                    "heat2": row.加熱爐2,
                    "heat3": row.加熱爐3,
                    "heat4": row.加熱爐4,
                    "heat5": row.加熱爐5,
                    "heat6": row.加熱爐6,
                    "heat7": row.加熱爐7,
                    "heat8": row.加熱爐8,
                    "heattemp": row.加熱爐油溫,
                    "heatsped": row.加熱爐速度,
                    "tempturing1": row.回火爐1,
                    "tempturing2": row.回火爐2,
                    "tempturing3": row.回火爐3,
                    "tempturing4": row.回火爐4,
                    "tempturing5": row.回火爐5,
                    "tempturing6": row.回火爐6,
                    "tempturisped": row.回火爐速度,
                    "furnstat": row.進爐狀態,
                    "produceday": row.製造日期,
                    "producetime": row.製造時間,
                    "control_man": control.id,
                    "qc": qc.id,
                    "shift": shift.id,
                    "ssk": row.斷面積,
                    "mxload1": row.最大負荷值1,
                    "mxload2": row.最大負荷值2,
                    "mxload3": row.最大負荷值3,
                    "mxload4": row.最大負荷值4,
                    "mxload5": row.最大負荷值5,
                    "mxload6": row.最大負荷值6,
                    "mxload7": row.最大負荷值7,
                    "mxload8": row.最大負荷值8,
                    "resist1": row.抗拉強度值1,
                    "resist2": row.抗拉強度值2,
                    "resist3": row.抗拉強度值3,
                    "resist4": row.抗拉強度值4,
                    "resist5": row.抗拉強度值5,
                    "resist6": row.抗拉強度值6,
                    "resist7": row.抗拉強度值7,
                    "resist8": row.抗拉強度值8,
                    "yield1": row.降伏點值1,
                    "yield2": row.降伏點值2,
                    "yield3": row.降伏點值3,
                    "yield4": row.降伏點值4,
                    "yield5": row.降伏點值5,
                    "yield6": row.降伏點值6,
                    "yield7": row.降伏點值7,
                    "yield8": row.降伏點值8,
                    "ystrength1": row.降伏強度值1,
                    "ystrength2": row.降伏強度值2,
                    "ystrength3": row.降伏強度值3,
                    "ystrength4": row.降伏強度值4,
                    "ystrength5": row.降伏強度值5,
                    "ystrength6": row.降伏強度值6,
                    "ystrength7": row.降伏強度值7,
                    "ystrength8": row.降伏強度值8,
                    "elong1": row.伸長率值1,
                    "elong2": row.伸長率值2,
                    "elong3": row.伸長率值3,
                    "elong4": row.伸長率值4,
                    "elong5": row.伸長率值5,
                    "elong6": row.伸長率值6,
                    "elong7": row.伸長率值7,
                    "elong8": row.伸長率值8,
                    "decarb1": row.脫碳層值1,
                    "decarb2": row.脫碳層值2,
                    "decarb3": row.脫碳層值3,
                    "decarb4": row.脫碳層值4,
                    "decarb5": row.脫碳層值5,
                    "decarb6": row.脫碳層值6,
                    "decarb7": row.脫碳層值7,
                    "decarb8": row.脫碳層值8,
                    "wxrhrd1": row.華司硬度值1,
                    "wxrhrd2": row.華司硬度值2,
                    "wxrhrd3": row.華司硬度值3,
                    "wxrhrd4": row.華司硬度值4,
                    "wxrhrd5": row.華司硬度值5,
                    "wxrhrd6": row.華司硬度值6,
                    "wxrhrd7": row.華司硬度值7,
                    "wxrhrd8": row.華司硬度值8,
                    "icritetia": row.國際標準,
                    "tensile_no": row.拉力機編號,
                    "sfhn": row.表面硬度規格,
                    "sfhv": row.表面硬度值,
                    "sfhv1": row.表面硬度值1,
                    "sfhv2": row.表面硬度值2,
                    "sfhv3": row.表面硬度值3,
                    "sfhv4": row.表面硬度值4,
                    "sfhv5": row.表面硬度值5,
                    "sfhv6": row.表面硬度值6,
                    "sfhv7": row.表面硬度值7,
                    "sfhv8": row.表面硬度值8,
                    "chn": row.心部硬度規格,
                    "chv": row.心部硬度值,
                    "chv1": row.心部硬度值1,
                    "chv2": row.心部硬度值2,
                    "chv3": row.心部硬度值3,
                    "chv4": row.心部硬度值4,
                    "chv5": row.心部硬度值5,
                    "chv6": row.心部硬度值6,
                    "chv7": row.心部硬度值7,
                    "chv8": row.心部硬度值8,
                    "rtens": row.抗拉強度值,
                    "rtenste": row.抗拉強度值起迄,
                    "ysv": row.降伏強度值,
                    "ysvste": row.降伏強度值起迄,
                    "elohv": row.伸長率值,
                    "elohvste": row.伸長率值起迄,
                    "yste": row.降伏點值起迄,
                    "mxloadste": row.最大負荷值起迄,
                    "sskste": row.斷面積值起迄,
                    "torshv": row.扭力強度值,
                    "torshv1": row.扭力強度值1,
                    "torshv2": row.扭力強度值2,
                    "torshv3": row.扭力強度值3,
                    "torshv4": row.扭力強度值4,
                    "torshv5": row.扭力強度值5,
                    "torshv6": row.扭力強度值6,
                    "torshv7": row.扭力強度值7,
                    "torshv8": row.扭力強度值8,
                    "carb1v": row.滲碳層1值,
                    "carb1v1": row.滲碳層1值1,
                    "carb1v2": row.滲碳層1值2,
                    "carb1v3": row.滲碳層1值3,
                    "carb1v4": row.滲碳層1值4,
                    "carb1v5": row.滲碳層1值5,
                    "carb1v6": row.滲碳層1值6,
                    "carb1v7": row.滲碳層1值7,
                    "carb1v8": row.滲碳層1值8,
                    "carb2v1": row.滲碳層2值1,
                    "carb2v2": row.滲碳層2值2,
                    "carb2v3": row.滲碳層2值3,
                    "carb2v4": row.滲碳層2值4,
                    "carb2v5": row.滲碳層2值5,
                    "carb2v6": row.滲碳層2值6,
                    "carb2v7": row.滲碳層2值7,
                    "carb2v8": row.滲碳層2值8,
                    "sskv": row.斷面收縮率值,
                    "sskv1": row.斷面收縮率值1,
                    "sskv2": row.斷面收縮率值2,
                    "sskv3": row.斷面收縮率值3,
                    "sskv4": row.斷面收縮率值4,
                    "sskv5": row.斷面收縮率值5,
                    "sskv6": row.斷面收縮率值6,
                    "sskv7": row.斷面收縮率值7,
                    "sskv8": row.斷面收縮率值8,
                    "safeload": row.安全負荷值,
                    "safeload1": row.安全負荷值1,
                    "safeload2": row.安全負荷值2,
                    "safeload3": row.安全負荷值3,
                    "safeload4": row.安全負荷值4,
                    "safeload5": row.安全負荷值5,
                    "safeload6": row.安全負荷值6,
                    "safeload7": row.安全負荷值7,
                    "safeload8": row.安全負荷值8,
                    "HV1": row.HV1,
                    "HV2": row.HV2,
                    "HV3": row.HV3,
                    "HV12": row.HV12,
                    "HV12OK": row.HV12OK,
                    "HV13": row.HV13,
                    "HV13OK": row.HV13OK,
                    "hs5": row.頭部敲擊5,
                    "hs10": row.頭部敲擊10,

                    "hs15": row.頭部敲擊15,
                    "curv5": row.彎曲度5,
                    "curv15": row.彎曲度15,
                    "wholeck": row.整體判定,
                    "faceck": row.外觀判定,
                    "ck_person": ck_person.id,
                    "singleton": row.單支重,
                    "uqbuckets": row.不合格桶數,
                    "uqtreat": row.不合格特急處理動作,
                    "produceday1": row.製造日期1,
                    "shift1": shift1.id,
                    "op1": op1.id,
                    "buckets1": row.桶數1,
                    "teamlead1": tm1.id,
                    "produceday2": row.製造日期2,
                    "shift2": shift2.id,
                    "op2": op2.id,
                    "buckets2": row.桶數2,
                    "teamlead2": tm2.id,
                    "produceday3": row.製造日期3,
                    "shift3": shift3.id,
                    "op3": op3.id,
                    "buckets3": row.桶數3,
                    "teamlead3": tm3.id,
                    "weighbuckets": row.磅後桶數,
                    "bdiff": row.桶數差,
                    "pweight": row.進貨重量,
                    "tweight": row.磅後總重,
                    "wdiff": row.重量差,

                    "currnt_furno": row.現在爐號,
                    "serial": row.序號,
                    "giveday": row.應對交期,
                    "ptime1": row.製造時間1,
                    "ptime2": row.製造時間2,
                    "ptime3": row.製造時間3,
                    "p_op": p_op.id,
                    "p_weight": p_weight.id,
                    "pnote": row.產量備註,
                    "ckresist": row.CK抗拉強度,
                    "cksurfhrd": row.CK表面硬度,
                    "ckcorehrd": row.CK心部硬度,
                    "ckcl": row.CK滲碳層,
                    "cksfhv": row.CK表面硬度值,
                    "ckchv": row.CK心部硬度值,
                    "ckrtens": row.CK抗拉強度值,
                    "ckyv": row.CK降伏強度值,
                    "ckelong": row.CK伸長率值,
                    "cktorsion": row.CK扭力強度值,
                    "ckcl1v": row.CK滲碳層1值,
                    "cksskv": row.CK斷面收縮率值,
                    "cksl": row.CK安全負荷值,
                    "ckysvste": row.CK降伏點值起迄,
                    "ckmlste": row.CK最大負荷值起迄,
                    "cksskste": row.CK斷面積值起迄,
                    "qcnote": row.品管備註,
                    "pw1": row.製造重量1,
                    "pw2": row.製造重量2,
                    "pw3": row.製造重量3,
                    "ckecl": row.CK脫碳層,
                    "ckecl2v": row.CK滲碳層2值,
                    "ckwhrd": row.CK華司硬度,
                    "ckhf": row.華司硬度規格,
                    "ffday": row.完爐日期,
                    "fftime": row.完爐時間,
                    "ckclv": row.CK滲碳層值,
                    "feedbucket": row.入料桶數,
                    "feedweight": row.入料總重,
                    "productname": productname.id,
                    "contrast": row.對照,
                    "shipbucket": row.出貨桶數,
                    "shipweight": row.出貨重量,
                    "sskvste": row.斷面收縮率值起迄,
                    "slste": row.安全負荷值起迄,
                    "ckhs": row.CK頭部敲擊,
                    "ckcurv": row.CK彎曲度,
                    "ckmxl": row.CK最大負荷,
                    "mxload": row.最大負荷,
                    "cktorsion": row.CK扭力強度,
                    "tlevel": row.扭力強度,
                    "ckwhrd1v": row.CK華司硬度1值,
                    "ckwhrd2v": row.CK華司硬度2值,
                    "whrd2v1": row.華司硬度2值1,
                    "whrd2v2": row.華司硬度2值2,
                    "whrd2v3": row.華司硬度2值3,
                    "whrd2v4": row.華司硬度2值4,
                    "whrd2v5": row.華司硬度2值5,
                    "whrd2v6": row.華司硬度2值6,
                    "whrd2v7": row.華司硬度2值7,
                    "whrd2v8": row.華司硬度2值8,
                    "uqtreat": row.不合格品處理,

                    "uqweight": row.不合格重量,
                    "followup": row.處理方式,
                    "clnorm": row.滲碳層規格,
                    "statecopy": row.狀態備份,
                    "amp1": row.圖倍率1,
                    "amp2": row.圖倍率2,
                    "amp3": row.圖倍率3,
                    "amp4": row.圖倍率4,
                    "amp5": row.圖倍率5,
                    "amp6": row.圖倍率6,
                    "mgreviewday": row.金相審核日期,
                    "mgcheckday": row.金相檢驗日期,
                    "mgreviewer": mgreviewer.id,
                    "mgchecker": mgchecker.id,
                    "mgrtell": row.金相結果判定說明,
                    "mgresult": row.金相結果判定,
                })
        except Exception as e:
            pass
        return True

    def insert_set_shift(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM s_一層代碼檔 WHERE 類別='S01N0006'")
            rows = cursor.fetchall()
            setshift = self.env["yc.setshift"].search([])
            sql = "delete from yc_setshift"
            self._cr.execute(sql)

            for row in rows:
                setshift.create({
                    "name": row.一層名稱,
                    "code": row.一層代碼,
                    "other1": row.參數1,
                    "other2": row.參數2,
                    "other3": row.參數3,
                })
        except Exception as e:
            pass
        return True

    def insert_set_length(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=220.133.113.223,1433; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM s_一層代碼檔 WHERE 類別='S03N0005'")
            rows = cursor.fetchall()
            setshift = self.env["yc.setlength"].search([])
            sql = "delete from yc_setlength"
            self._cr.execute(sql)

            for row in rows:
                setshift.create({
                    "name": row.一層名稱,
                    "code": row.一層代碼,
                    "parameter1": row.參數1,
                    "parameter2": row.參數2,
                    "parameter3": row.參數3,
                })
        except Exception as e:
            pass
        return True

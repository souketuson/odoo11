# -*- coding: utf-8 -*-

import logging, pyodbc, time, collections, math
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class YcDataImport(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'yc.data.import'

    how_many_do_you_want = fields.Char("匯入筆數", help='輸入整數數字\n-1: 匯入全部筆數')

    # 開始連線
    def _connection_start(self):
        self.cnxn = pyodbc.connect(
            'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
        return self.cnxn.cursor()

    # 結束連線
    def _disconnction(self):
        self.cnxn.close()
        print(' \033[42m \033[0m 資料庫連線已結束.')
        time.sleep(5)

    # 時間轉換
    def _time_formater(self, sec):
        _hour = math.floor(sec / 3600)
        _min = math.floor((sec / 60) - (_hour * 60))
        _sec = (sec - (3600 * _hour + 60 * _min))
        if sec >= 3600:
            _time = '%s小時%s分%d' % (_hour, _min, _sec)
        elif sec < 3600 and sec >= 60:
            _time = '%s分%d秒' % (_min, _sec)
        else:
            _time = '%d秒' % (_sec)
        return _time

    # 匯入員工資料
    # ps. 如果在odoo裡面欄位性質是x2x 只能填寫ID進去資料庫
    def employee(self):
        feet = 0
        traveler = self.env['res.users']
        goal = int(self.how_many_do_you_wants)
        try:
            self._connection_start()
            cursor = self.cnxn.cursor()
            cursor.execute('SELECT * FROM 員工主檔')
            sql = "DELETE FROM res_users WHERE user_class='1'"
            self._cr.execute(sql)
            init = time.time()
            print(" \033[42m \033[0m 開始建立資料")
            while 1:
                row = cursor.fetchone()
                if goal == feet or (goal < 0 and goal != -1) or not row:
                    break
                feet += 1
                print(' \033[43m \033[0m [' + str(feet) + '] 建立:' + row.姓名)
                traveler.create({
                    "login": row.員工代號, "password": row.密碼,
                    # 分廠要用factory還是res.company model
                    # "factory_id": factory_id_check.id,
                    # "dep_id": dep_id_check.id,
                    # "employee_type": row.僱用性質代碼,
                    "title1": row.職稱代碼1, "title2": row.職稱代碼2,
                    "title3": row.職稱代碼3, "name": row.姓名, "gender": row.性別,
                    "idcard": row.身份證號, "birthday": row.出生日期,
                    "birthplace": row.籍貫, "marrige": row.婚姻, "kids": row.子女數,
                    "phone": row.電話, "mobile": row.手機, "email": row.E_Mail,
                    "addr_mail": row.通訊地址, "addr_born": row.戶籍地址,
                    "ecp": row.緊急聯絡人, "rel_ecp": row.關係, "em_phone": row.聯絡電話,
                    "em_mobile": row.聯絡手機, "date_duty": row.到職日期,
                    "date_leave": row.離職日期, "note": row.備註,
                    "last_log": row.最後登入時間, "log_state": row.登入否,
                    "user_class": '1',
                })
            print(' \033[42m \033[0m 資料建立完成，總完成筆數:%s' % feet)
            self._disconnction()
        except Exception as e:
            print(' \033[41m \033[0m Oops!\n %s' % e)
            self._disconnction()
            pass
        end = time.time()
        delta = self._time_formater((end - init))
        print(' \033[42m \033[0m 用時%s' % delta)
        return True

    # 過磅單、過磅單項目檔；進貨單、進貨單項目檔
    # constrain 和 create method check要關掉
    def weight_main(self):
        feet = 0
        traveler = self.env['yc.weight']
        goal = int(self.how_many_do_you_want)
        try:
            self._connection_start()
            cursor = self.cnxn.cursor()
            cursor.execute('SELECT * FROM 過磅單主檔')
            sql = "DELETE FROM yc_weight"
            self._cr.execute(sql)
            init = time.time()
            print(" \033[42m \033[0m 開始建立過磅主檔資料")
            while 1:
                row = cursor.fetchone()
                driver = self.env["yc.driver"].search([("code", '=', row.司機代號)])
                if any(driver):
                    driver_id = driver.id
                else:
                    self.env['yc.driver'].create({'name':row.司機代號})
                    print("新增一筆司機資料")
                    driver_id = driver.search([('name', '=', row.司機代號)])
                person = self.env["yc.hr"].search([("code", '=', row.過磅人員)])
                if any(person):
                    person_id = person.id
                else:
                    self.env['res.users'].create({'name': row.過磅人員,
                                                  "user_class": '1'})
                    print("新增一筆員工資料")
                    person_id = person.search([("code", '=', row.過磅人員)])
                factory = self.env["yc.factory"].search([("name", '=', row.所屬工廠)])
                if any(factory):
                    factory_id = factory.id
                if goal == feet or (goal < 0 and goal != -1) or not row:
                    break

                feet += 1
                print(' \033[43m \033[0m [' + str(feet) + '] 主檔單號:' + row.過磅單號)
                traveler.create({
                    "name": row.過磅單號, "in_out": row.分類,
                    "driver_id": driver_id, "day": row.日期,
                    "weightime": row.時間, "carno": row.車次序號,
                    "person_id": person_id, "weighbridge": row.地磅序號,
                    "plate_no": row.車號, "refine": row.調質重量,
                    "total": row.總重, "carbur": row.滲碳重量,
                    "curbweight": row.空車重, "other": row.其他重量,
                    "emptybucket": row.空桶重, "net": row.淨重,
                    "purchase_times": row.進貨次數, "ship_times": row.出貨次數,
                    "note": row.備註, "other1": row.其他重量1, "factory_id": factory_id,
                })
            print(' \033[42m \033[0m 資料建立完成，總完成筆數:%s' % feet)
            self._disconnction()
        except Exception as e:
            print(' \033[41m \033[0m Oops!\n %s' % e)
            self._disconnction()
            pass
        end = time.time()
        delta = self._time_formater((end - init))
        print(' \033[42m \033[0m 用時%s' % delta)
        return True

    # 過磅單主檔
    @api.multi
    def insert_weight_main(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
                if row.司機代號 and driver_id and person_id:
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
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
        insert_weight_main = YcDataImport.insert_weight_main
        insert_weight_details = YcDataImport.insert_weight_details
        funcs = insert_weight_main, insert_weight_details
        for func in funcs:
            func(self)

    @api.multi
    def insert_yc_sets01(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor_dict = collections.OrderedDict()
            cursor_dict['S01N0001'] = ["rows_factory", "yc.factory"]
            cursor_dict['S01N0002'] = ["rows_department", "yc.department"]
            cursor_dict['S01N0004'] = ["jobtitle", "yc.setjobtitle"]
            cursor_dict['S01N0005'] = ["salaryitem", "yc.setsalaryitem"]
            cursor_dict['S01N0006'] = ["shift", "yc.setshift"]
            cursor_dict['S01N0007'] = ["leave", "yc.setleave"]
            cursor_dict['S01N0008'] = ["bonus", "yc.setbonus"]

            for key, item in cursor_dict.items():
                t_sql = "SELECT * FROM s_一層代碼檔 WHERE 類別='%s'" % key
                cursor.execute(t_sql)
                rows = cursor.fetchall()

                var = item[0]
                search = self.env["%s" % item[1]].search([])
                # str covert to variable
                exec("%s = %s" % (var, 0))
                # assign dbview to variable
                var = search
                sql = "delete from %s" % item[1].replace('.', '_')

                self._cr.execute(sql)
                for row in rows:
                    if key == "S01N0001":
                        var.create({
                            "name": row.一層名稱,
                            "code": row.一層代碼,
                            "params1": row.參數1,
                        })
                    elif key == "S01N0002" or "S01N0004" or "S01N0005" or "S01N0007" or "S01N0008":
                        var.create({
                            "name": row.一層名稱,
                            "code": row.一層代碼,
                        })
                    elif key == "S01N0006":
                        var.create({
                            "name": row.一層名稱,
                            "code": row.一層代碼,
                            "other1": row.參數1,
                            "other2": row.參數2,
                        })
        except Exception as e:
            pass
        return True

    @api.multi
    def insert_yc_sets04(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor_dict = collections.OrderedDict()
            cursor_dict['S04N0001'] = ["rows_producenote", "yc.setproducenote"]
            # cursor_dict['S04N0002'] = ["rows_department", "yc.department"] already have setstrength table
            cursor_dict['S04N0003'] = ["rows_hardness", "yc.sethardness"]
            cursor_dict['S04N0004'] = ["rows_qcnote", "yc.setqcnote"]

            for key, item in cursor_dict.items():
                t_sql = "SELECT * FROM s_一層代碼檔 WHERE 類別='%s'" % key
                cursor.execute(t_sql)
                rows = cursor.fetchall()

                var = item[0]
                search = self.env["%s" % item[1]].search([])
                # str covert to variable
                exec("%s = %s" % (var, 0))
                # assign dbview to variable
                var = search
                sql = "delete from %s" % item[1].replace('.', '_')

                self._cr.execute(sql)
                for row in rows:
                    var.create({
                        "name": row.一層名稱,
                        "code": row.一層代碼,
                        "parameter1": row.參數1,
                        "parameter2": row.參數2,
                        "parameter3": row.參數3,
                    })
        except Exception as e:
            pass
        return True

    # 司機主檔轉資料庫 ERPALL > pgsql
    @api.multi
    def insert_yc_driver(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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

    @api.multi
    def insert_processing(self):
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
            'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
    #             'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM 產品機械性質主檔")
            rows = cursor.fetchall()
            mp = self.env["yc.mechanicalproperty"]
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
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
            cursor = cnxn.cursor()

            # 要拉出在過磅單有出現的單子
            # SQL strict form: SELECT * FROM 資料表 WHERE 欄位 IN('xxxxxxxxx','oooooo')
            weight = self.env["yc.weight"].search([])
            _string = ''
            for x in range(len(weight)):
                if x != len(weight) - 1:
                    _string += "'" + weight[x].carno + "',"
                else:
                    _string += "'" + weight[x].carno + "'"
            db_sql = "SELECT * FROM 進貨單主檔 WHERE 車次序號 IN(%s)" % _string
            cursor.execute(db_sql)
            rows = cursor.fetchall()
            purchase = self.env["yc.purchase"].search([])
            sql = "delete from yc_purchase"
            self._cr.execute(sql)
            for row in rows:
                for x in range(len(row)):
                    if row[x] != None and type(row[x]) == str:
                        row[x] = row[x].rstrip(' ')
                        row[x] = row[x].lstrip(' ')

                driver = self.env["yc.driver"].search([("code", "=", row.司機代號)])
                # processing = self.env["yc.processing"].search([("code", "=", row.加工廠代號)])
                processing = self.env["yc.processing"].search([("code", "=", row.所屬工廠)])
                factory = self.env["yc.factory"].search([("name", "=", row.所屬工廠)])
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
                status = self.env["yc.setstatus"].search([("code", "=", row.狀態)])
                sfhn = self.env["yc.sethardness"].search([("name", "=", row.表面硬度規格)])
                chn = self.env["yc.sethardness"].search([("name", "=", row.心部硬度規格)])
                ckhf = self.env["yc.sethardness"].search([("name", "=", row.華司硬度規格)])

                purchase.create({
                    "name": row.工令號碼,
                    "day": row.進貨日期,
                    "time": row.時間,
                    "status": status.id,
                    "weighstate": row.過磅狀態,
                    "checkstate": row.檢驗狀態,
                    "driver_id": driver.id,
                    "factory_id": factory.id,
                    "processing_attache": processing.id,
                    "pre_order": row.前工令號碼,
                    # 這個要丟單號還是車次號碼?
                    "car_no": carno.id,
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
                    "ptime": row.製造時間,
                    "op": control.id,
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
                    "sfhn": sfhn.id,
                    "sfhv": row.表面硬度值,
                    "sfhv1": row.表面硬度值1,
                    "sfhv2": row.表面硬度值2,
                    "sfhv3": row.表面硬度值3,
                    "sfhv4": row.表面硬度值4,
                    "sfhv5": row.表面硬度值5,
                    "sfhv6": row.表面硬度值6,
                    "sfhv7": row.表面硬度值7,
                    "sfhv8": row.表面硬度值8,
                    "chn": chn.id,
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
                    "uqemtreat": row.不合格特急處理動作,
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
                    "cktv": row.CK扭力強度值,
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
                    "ckhf": ckhf.id,
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

    # def insert_set_shift(self):
    #     try:
    #         cnxn = pyodbc.connect(
    #             'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
    #         cursor = cnxn.cursor()
    #         cursor.execute("SELECT * FROM s_一層代碼檔 WHERE 類別='S01N0006'")
    #         rows = cursor.fetchall()
    #         setshift = self.env["yc.setshift"].search([])
    #         sql = "delete from yc_setshift"
    #         self._cr.execute(sql)
    #
    #         for row in rows:
    #             setshift.create({
    #                 "name": row.一層名稱,
    #                 "code": row.一層代碼,
    #                 "other1": row.參數1,
    #                 "other2": row.參數2,
    #                 "other3": row.參數3,
    #             })
    #     except Exception as e:
    #         pass
    #     return True

    def insert_set_length(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server}; SERVER=192.168.2.102; DATABASE=ERPALL; UID=erplogin; PWD=@53272162')
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

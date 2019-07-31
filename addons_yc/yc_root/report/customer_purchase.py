# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YcCargo(models.TransientModel):
    _name = 'yc.cargo'
    driver_id = fields.Many2one("yc.driver", string="司機名稱")
    year = fields.Char()
    month = fields.Char()



    def get_report(self):
        if self.driver_id:
            data = {
                'ids': self.ids,
                'model': self._name,
                'form': {
                    'driver_id': self.driver_id.id,
                    'driver_name': self.driver_id.name,
                    'date_start': self.date_start,
                    'date_end': self.date_end,
                },
            }
            # use `module_name.report_id` as reference.
            # `report_action()` will call `get_report_values()` and pass `data` automatically.
            return self.env.ref('yc_root.action_yc_cargo_report').report_action(self, data=data)

class YcCargoReport(models.AbstractModel):
    '''restrict form "report.module_name.template_id"'''

    _name = 'report.yc_root.yc_cargo_report_view'

    @api.model
    def get_report_values(self, docids,data=None):
        driver =  data['form']['driver_id']
        driver_name = data['form']['driver_name']
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        docs = []
        # 姓名            統計日期-s-e       頁次
        # 日期 時間 地磅序號 重量 單價 金額 備註 類別
        domain = [('driver_id','=', driver),
                  ('day', '>=', date_start),
                  ('day', '<=', date_end)]
        records = self.env['yc.weight'].search(domain, order='day asc')
        for rec in records:
            details = self.env['yc.weight.details']
            x_list = ['%s %s' % (name.processing_id.abbrev.rstrip(), name.customer_id.abbrev.rstrip()) for name in details.search([('name', '=', rec.id)])]
            note = ''.join(';'.join(x_list))

            io = rec.in_out
            if not bool(io):
                raise Exception('in_out 無值')
            docs.append({
                'day': rec.day,
                'time': rec.weightime,
                'weighbridge': rec.weighbridge,
                'net': rec.net,
                'per_price': 0.000,
                'tt_price': 0,
                'note': note,
                'type': '進貨' if io == 'I' else '出貨',
            })

        return { 'doc_ids': data['ids'],
                 'doc_model': data['model'],
                 'driver_name': driver_name,
                 'date_start': date_start,
                 'date_end': date_end,
                 'docs':docs}
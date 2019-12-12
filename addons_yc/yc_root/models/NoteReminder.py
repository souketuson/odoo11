# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime as dt
import pytz, logging, collections, re


class YcPurchase(models.Model):
    _inherit = "yc.purchase"

    # 依上一筆資料預設該欄位資料功能
    # 欄位: 備註*9、材質、規格、強度級數、加工方式

    @api.model
    def create(self, vals):
        _action = self.env['ir.actions.act_window']
        p1 = _action.search([('name', '=', '進貨單作業')], limit=1).id
        # 將這次備註的資料存進資料庫，下一次打單自動讀取
        if self._context.get('params')['action'] == p1:
            # strength_level
            # norm_code
            # txtur_code
            # proces_code
            sl = None if not vals.get('strength_level') else vals['strength_level']
            norm = None if not vals.get('norm_code') else vals['norm_code']
            txt = None if not vals.get('txtur_code') else vals['txtur_code']
            prc = None if not vals.get('proces_code') else vals['proces_code']
            reminder = {'strength_level': sl, 'norm_code': norm, 'txtur_code': txt, 'proces_code': prc}
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', self.env.user.id)])
            note = ['notices1', 'notices2', 'notices3', 'qcnote1', 'qcnote2', 'qcnote3', 'prodnote1', 'prodnote2',
                    'prodnote3', ]

            note_dictionary = self.env['yc.setpurchasenote']
            for n in note:
                if vals.get(n):
                    # 確認這個note是否有在資料庫
                    vocabulary = note_dictionary.search([('name', '=', vals[n])])
                    if vocabulary:
                        reminder.update({n: vocabulary.id})
                    else:
                        pass
                else:
                    reminder.update({n: None})
            if rec:
                rec.write(reminder)
            else:
                reminder.update({'user': self.env.user.id})
                rec.create(reminder)
        return super(YcPurchase, self).create(vals)

    # 備註自動抓取上一次使用的值
    def _n1deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.notices1.name
            else:
                return None

    def _n2deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.notices2.name
            else:
                return None

    def _n3deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.notices3.name
            else:
                return None

    def _qcn1deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.qcnote1.name
            else:
                return None

    def _qcn2deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.qcnote2.name
            else:
                return None

    def _qcn3deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.qcnote3.name
            else:
                return None

    def _pn1deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.prodnote1.name
            else:
                return None

    def _pn2deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.prodnote2.name
            else:
                return None

    def _pn3deault(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.prodnote3.name
            else:
                return None

    def _last_strength(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.strength_level.id
            else:
                return None

    def _last_norm(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.norm_code.id
            else:
                return None

    def _last_txtur(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.txtur_code.id
            else:
                return None

    def _last_proces(self):
        _action = self.env['ir.actions.act_window']
        page = _action.search([('name', '=', '進貨單作業')], limit=1).id
        if self._context['params'].get('action') == page:
            user = self.env.user.id
            db = self.env['yc.setnotereminder']
            rec = db.search([('user', '=', user)])
            if rec:
                return rec.proces_code.id
            else:
                return None


class YcSetnotereminder(models.Model):
    _name = "yc.setnotereminder"
    # 欄位: 備註*9、材質、規格、強度級數、加工方式
    user = fields.Many2one("res.users", string="開單人員")
    strength_level = fields.Many2one("yc.setstrength", string="強度級數")
    norm_code = fields.Many2one("yc.setnorm", string="規格")
    txtur_code = fields.Many2one("yc.settexture", string="材質")
    proces_code = fields.Many2one("yc.setprocess", string="加工方式")
    notices1 = fields.Many2one('yc.setpurchasenote')
    notices2 = fields.Many2one('yc.setpurchasenote')
    notices3 = fields.Many2one('yc.setpurchasenote')
    prodnote1 = fields.Many2one('yc.setpurchasenote')
    prodnote2 = fields.Many2one('yc.setpurchasenote')
    prodnote3 = fields.Many2one('yc.setpurchasenote')
    qcnote1 = fields.Many2one('yc.setpurchasenote')
    qcnote2 = fields.Many2one('yc.setpurchasenote')
    qcnote3 = fields.Many2one('yc.setpurchasenote')

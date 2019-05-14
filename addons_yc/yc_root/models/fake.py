# -*- coding: utf-8 -*-


from odoo import models, fields, api


class YcFake(models.Model):
    _name = "yc.fake"
    _description = 'Book'
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    author_ids = fields.Many2many('res.partner', string='Authors')

    img = fields.Binary("image", attachment=True)
    img_attch = fields.Char("url", compute="_get_img_html")

    @api.multi
    def _get_img_html(self):
        if self.img:
            for elem in self:
                # /web/content/<string:model>/<int:id>/<string:field>/<string:filename> refer to addons/web/controllers/main.py
                # ir_at = elem.env["ir.attachment"].search([("res_model","=", "yc.fake")])
                img_url = '/web/content/'
                elem.img_attch = '<img src="%s"/>' % img_url

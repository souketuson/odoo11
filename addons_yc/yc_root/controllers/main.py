# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http
from datetime import datetime as dt
import pytz

class GetMatchingRecords(http.Controller):

    @http.route("/note_search", type="json", auth="public", website=True)
    def note_search(self, txt):
        """
        Remote Procedure Call:
        Seraching for the corresponding lot and then search for note id/name.
        Return them to the website form through ajax.
        """
        domain = [("name", "ilike", txt)]
        records = request.env["yc.setpurchasenote"].sudo().search(domain)

        if not records:
            return {"fail": True}

        suggestions = []
        for record in records:
            vals = {}
            vals['value'] = record.name
            suggestions.append(vals)
        return suggestions

    @http.route("/cokoo", type="json", auth="public", website=True)
    def cokoo(self):
        now = dt.now(pytz.timezone('Asia/Taipei')).strftime("%Y%m%d%H%M%S")
        time = '%s:%s:%s' % (now[8:10], now[10:12], now[12:14])
        return time

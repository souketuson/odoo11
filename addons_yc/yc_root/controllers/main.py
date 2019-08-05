# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http

class GetMatchingRecords(http.Controller):

    @http.route("/serial_search", type="json",auth="public", website=True)
    def serial_search(self, serial):
        """
        Starting from a serial number (portal user input),
        serach for the corresponding lot and then search
        for product id/name and brand id/name.
        Return them to the website form.
        """
        serial_domain = [("name", "ilike", serial)]
        serial_objs = request.env["yc.setpurchasenote"].sudo().search(serial_domain)

        if not serial_objs:
            return {"fail": True}

        suggestions = []
        for serial_obj in serial_objs:
            serial_vals = {}
            serial_vals['value'] = serial_obj.name
            suggestions.append(serial_vals)
        return suggestions
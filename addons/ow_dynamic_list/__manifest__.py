# -*- coding: utf-8 -*-
# Part of OdooWare. See LICENSE file for copyright and licensing details.
{
    'name': 'Dynamic List V11',
    'version': '1.1.1',
    'author': 'OdooWare',
    'category': 'Tools',
    'website': 'https://Odooware.com',
    'summary': 'Arrange any List view on the fly for odoo v11',
    'description': """
        Arrange any List view on the fly without any technical knowledge.
    """,
    'depends': ['web'],
    'price': 249.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'data': [
        "security/ir.model.access.csv", 
        'views/dynamic_list_view.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': ['static/src/xml/dynamic_list.xml'],
    'images': ['static/description/ow_dynamic_list_banner.png'],
}
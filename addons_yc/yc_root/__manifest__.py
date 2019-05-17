# -*- coding: utf-8 -*-
{
    'name': "yc_root",

    'summary': """
    """,

    'description': """
        YC_ROOT v.10
    """,

    'author': "ArJhe",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'views/quantity_data_entry.xml',
        'views/process_data_entry.xml',
        'views/produce/plan_furna.xml',
        'views/produce/furna_import.xml',
        'views/produce/purchase.xml',
        'views/produce/weight.xml',
        'views/produce/purchase_store.xml',
        'views/produce/purchase_report.xml',
        # 'wizard/purchase_report.xml',

        'views/produce/maintain/setproduct.xml',
        'views/produce/maintain/setstrength.xml',
        'views/produce/maintain/setnorm.xml',
        'views/produce/maintain/setlength.xml',
        'views/quality/maintain/setproducenote.xml',
        'views/quality/maintain/sethardness.xml',
        'views/quality/maintain/setqcnote.xml',
        'views/maintain/factory.xml',
        'views/maintain/department.xml',
        'views/maintain/setjobtitle.xml',
        'views/maintain/setsalaryitem.xml',
        'views/maintain/setshift.xml',
        'views/maintain/setleave.xml',
        'views/maintain/setbonus.xml',
        'views/mechanicalproperty.xml',
        'views/driver.xml',
        'views/hr_main.xml',
        'views/quality.xml',
        'views/fake.xml',

        'menuitem/root_core.xml',

    ],
    'css': ['static/src/css/cssfile.css',
            ],

    # only loaded in demonstration mode
    'demo': [

    ],
}

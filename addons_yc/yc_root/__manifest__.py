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
    'css': [
        'static/src/css/generalcss.css',

    ],
    'data': [
        'report/purchase_report.xml',
        'wizard/purchase_wizard.xml',
        'wizard/purchase_preorder.xml',
        'wizard/shipment_wizard.xml',
        'views/business/maintain/setprocessingareatype.xml',
        'views/business/maintain/setprocessingplanttype.xml',
        'views/business/maintain/setcurrency.xml',
        'views/business/maintain/setpayment.xml',
        'views/business/maintain/setsuppliertype.xml',
        'views/business/maintain/setcustomertype.xml',
        'views/business/supplier.xml',
        'views/business/customer.xml',
        'views/business/process1.xml',
        'views/business/process2.xml',
        'views/shipment.xml',
        'views/quantity_data_entry.xml',
        'views/process_data_entry.xml',
        'views/produce/plan_furna.xml',
        'views/produce/furna_import.xml',
        'views/produce/purchase.xml',
        'views/produce/weight.xml',
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

    # only loaded in demonstration mode
    'demo': [

    ],
}

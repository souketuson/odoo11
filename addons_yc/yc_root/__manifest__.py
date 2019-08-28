# -*- coding: utf-8 -*-
{
    'name': "yc_root",

    'summary': """
    """,

    'description': """
        last update: 20190814
    """,
    'author': "ArJhe",
    'website': "",
    'category': 'Uncategorized',
    'version': '1.6',
    'depends': ['base'],
    'css': [
        'static/src/css/generalcss.css',

    ],
    'data': [
        # 'abandon/quantity_data_entry.xml',
        # 'abandon/process_data_entry.xml',
        # 'abandon/plan_furna.xml',
        # 'abandon/furna_import.xml',
        # 'abandon/qcnote_wizard.xml',
        # 'abandon/quality.xml',
        # 'abandon/factory.xml',
        'views/produce/maintain/setproduct.xml',
        'views/produce/maintain/setstrength.xml',
        'views/produce/maintain/setnorm.xml',
        'views/produce/maintain/setlength.xml',
        'views/produce/maintain/setstoreplace.xml',
        'views/produce/maintain/setpurchasenote.xml',
        'views/quality/maintain/setproducenote.xml',
        'views/quality/maintain/sethardness.xml',
        'views/quality/maintain/setqcnote.xml',

        'views/maintain/department.xml',
        'views/maintain/setjobtitle.xml',
        'views/maintain/setsalaryitem.xml',
        'views/maintain/setshift.xml',
        'views/maintain/setleave.xml',
        'views/maintain/setbonus.xml',
        'views/business/maintain/setprocessingareatype.xml',
        'views/business/maintain/setprocessingplanttype.xml',
        'views/business/maintain/setcurrency.xml',
        'views/business/maintain/setpayment.xml',
        'views/business/maintain/setsuppliertype.xml',
        'views/business/maintain/setcustomertype.xml',

        'views/general_view.xml',
        'report/purchase_report.xml',
        'report/furna_order.xml',
        'report/furna_quality.xml',
        'report/quality_sample.xml',
        'report/quality_examine_report.xml',
        'report/quality_unqualified_treatment.xml',
        'report/weight_order1.xml',
        'report/weight_order_test.xml',
        'report/cargo.xml',
        'report/cargo_report.xml',

        'wizard/process_review.xml',
        'wizard/quantity_review.xml',
        'wizard/weight_wizard.xml',
        'wizard/order_display.xml',
        'wizard/order_display_wizard.xml',
        'wizard/purchase_wizard.xml',
        'wizard/purchase_preorder.xml',
        'wizard/shipment_wizard.xml',
        'wizard/quality_wizard.xml',
        # 'wizard/quality_invalid.xml',

        'views/business/supplier.xml',
        'views/business/customer.xml',
        'views/business/process1.xml',
        'views/business/process2.xml',
        'views/shipment.xml',
        # 'views/produce/purchase.xml',
        'views/produce/pretreat.xml',
        'views/produce/purchase2.xml',
        'views/produce/weight.xml',
        'views/produce/return.xml',

        'views/mechanicalproperty.xml',

        'views/driver.xml',
        'views/hr_main.xml',

        'views/fake.xml',
        'menuitem/root_core.xml',
    ],

    # only loaded in demonstration mode
    'demo': [

    ],
}

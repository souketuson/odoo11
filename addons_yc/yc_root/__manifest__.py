{
    'name': "yc_root",

    'summary': """
    """,

    'description': """
        YC_ROOT v.6
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
        'views/produce/maintain/setproduct.xml',
        'views/driver.xml',
        'views/hr_main.xml',
        'views/fake.xml',

        'menuitem/root_core.xml',

    ],
    'css': ['static/src/css/cssfile.css'],

    # only loaded in demonstration mode
    'demo': [

    ],
}

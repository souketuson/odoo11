{
    'name': "yc_produce",

    'summary': """
        軟體的文字說明
    """,

    'description': """
        製造
    """,

    'author': "ArJhe",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'views/weight_cargo.xml',
        'views/purchase.xml',
        'menuitem/produce_core_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
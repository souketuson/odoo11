{
    'name': "yc_hr",

    'summary': """
        軟體的文字說明a
    """,

    'description': """
        軟體更長的文字說明
    """,

    'author': "ArJhe",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'views/hr_main.xml',
        'views/driver.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
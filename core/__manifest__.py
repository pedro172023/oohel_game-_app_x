# -*- coding: utf-8 -*-
{
    'name': "Oohel - App",
    'summary': """
      Módulo core de app
    """,
    'description': """
       Se crean los modelos de catálogos que se actualizan desde el ERP a Dentalia y viceversa. 
    """,
    'author': "",
    'website': "http://oohel.net/",
    'category': 'Tools',
    'version': '14.0.1',

    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        # parameters
        'data/params.xml',
        # views
        'views/tokens.xml',
        'wizards/settings.xml',
    ],
    'qweb': [
        # 'static/src/xml/mercado_pago.xml',
    ],
    'post_init_hook': "post_init_hook",
}

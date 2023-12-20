{
    'name': 'Módulo para notificaciones push',
    'version': '14.0.1',
    'summary': 'Se podran enviar notificaciones a los dispositivos de los usuarios',
    'category': 'Apps Mobiles',
    'author': 'Pedro Sanchez H. <pedro.sanchez@oohel.net>, pedro172023',
    'website': 'https://www.oohel.net/',
    'contributors': [],
    'depends': [
        'base',
        'base_setup',
    ],
    'data': [
        'data/action_planificada_remove_tokens.xml',
        'security/ir.model.access.csv',
        'views/notification_push.xml',
        'views/user_notification_push.xml',
        'views/aviso_notification_push.xml',
        'views/segmento_notification_push.xml',
        'data/params.xml',
        'wizard/config_settings.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

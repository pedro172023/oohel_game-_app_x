{
    'name': 'Game',
    'version': '14.0.1',
    'summary': 'Servicios para la aplicación game.',
    'description': 'Servicios para la aplicación game',
    'category': 'Game',
    'author': '',
    'website': 'https://oohel.net',
    'license': 'GPL-3',
    'depends': [
        'jsonifier',
        'maintenance',
        'oohel_notification_push',
        'core'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/activity_enviar_preguntas_accion_uno.xml',
        'data/accion_dos_activity_enviar_preguntas.xml',
        'views/user.xml',
        'wizard/asignacion_puntos.xml',
        'wizard/registrar_preguntas.xml',
        'wizard/asignacion_de_premios.xml',
        'views/premio.xml',
        'views/menu.xml'
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False
}

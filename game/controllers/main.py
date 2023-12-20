"""
@autor: Pedro Sánchez H. <pedro.sanchez@oohel.net>
@date: 19/12/2023
@name: main.py
"""
import logging
from odoo.addons.core.libs.response import valid_token, makeResponse, STATES, badRequest, JsonResponse
from odoo.http import route, request, Controller
logger = logging.getLogger(__name__)


class MainControllerCoreApp(Controller):
    """
        Controlador principal para la app
    """
    @route('/api/v1/saldo', method=['GET'], cors='*', csrf=False, auth="none", type="http", website=False)
    @valid_token
    def get_saldo(self, **post):
        user = post['token']['usuario_id']
        saldo = user.get_saldo()
        return makeResponse(
            state=STATES['SUCCESS'],
            message='Saldo',
            data=saldo,
        )

    @route('/api/v1/pregunta', method=['GET'], cors='*', csrf=False, auth="none", type="http", website=False)
    @valid_token
    def get_pregunta_activa(self, **post):
        user = post['token']['usuario_id']
        # pregunta = user.get_pregunta_activa()
        pregunta = '¿Que tiene el rey en la panza?'
        return makeResponse(
            state=STATES['SUCCESS'],
            message='Pregunta',
            data=pregunta,
        )

    @route('/api/v1/pregunta/<int:pregunta_id>', method=['PUT', 'OPTIONS'],
           cors='*',
           csrf=False,
           auth="none", type="http",
           website=False)
    @valid_token
    def set_update_pregunta(self, pregunta_id=None, **post):
        logger.info(post)
        user = post['token']['usuario_id']
        del post['token']
        # request.env
        if not pregunta_id:
            return JsonResponse(state=STATES['BAD_REQUEST'], message='El ID de la solicitud es requerido')
        # pregunta = request.env['oohel.pregunta'].browse(pregunta_id)
        pregunta = True
        print(pregunta_id)
        print(post.get('respuesta'))
        # if not pregunta.exists():
        #     return JsonResponse(
        #         state=STATES['NOT_FOUND'],
        #         message='La solicitud de mantenimiento no existe'
        #     )
        # pregunta.sudo().write(post)
        return JsonResponse(
            state=STATES['SUCCESS'],
            message='Success',
            data=pregunta
            # data=pregunta.get_solicitud(),
        )
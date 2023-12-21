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
        pregunta_str = ''
        dinero_str = ''
        pregunta_id = ''
        completada = False
        pregunta = request.env['oohel.pregunta_game'].sudo().search([('activo', '=', True)], limit=1)
        if pregunta:
            pregunta_str = pregunta.pregunta
            dinero_str = pregunta.dinero_ficticio
            pregunta_id = pregunta.id
            participacion = request.env['oohel.participacion_game'].sudo().search(
                [('pregunta_id', '=', pregunta_id), ('user_id', '=', user.id)])
            completada = True if participacion else False
        return makeResponse(
            state=STATES['SUCCESS'],
            message='Pregunta',
            data={'id': pregunta_id, 'pregunta': pregunta_str, 'dinero_ficticio': dinero_str, 'completada': completada}
        )

    @route('/api/v1/pregunta/<int:pregunta_id>', method=['PUT', 'OPTIONS'],
           cors='*',
           csrf=False,
           auth="none", type="http",
           website=False)
    @valid_token
    def set_update_pregunta(self, pregunta_id=None, **post):
        mensaje = ''
        maximo_ganadores = 2
        logger.info(post)
        user = post['token']['usuario_id']
        del post['token']
        if not pregunta_id:
            return JsonResponse(state=STATES['BAD_REQUEST'], message='El ID de la solicitud es requerido')
        pregunta = request.env['oohel.pregunta_game'].browse(int(pregunta_id))
        if pregunta.activo:
            participante_pregunta = request.env['oohel.participacion_game'].sudo().search(
                [('user_id', '=', user.id), ('pregunta_id', '=', pregunta_id)])
            if participante_pregunta:
                mensaje = 'Ya has respondido esta pregunta'
            else:
                numero_participantes = len(pregunta.participacion_ids.filtered(lambda x: x.correcta == True))
                if numero_participantes >= maximo_ganadores:
                    mensaje = f'Ya no puedes participar, por que ya existen {maximo_ganadores} ganadores'
                else:
                    correcto = True if post.get('respuesta').lower() == pregunta.respuesta.lower() else False
                    request.env['oohel.participacion_game'].sudo().create({
                        'pregunta_id': pregunta_id,
                        'user_id': user.id,
                        'respuesta': post.get('respuesta'),
                        'correcta': correcto
                    })
                    if correcto:
                        operacion_user = request.env['oohel.operacion_game'].sudo().create({
                            'titulo': 'Ganador de una pregunta rapida',
                            'user_id': user.id,
                            'dinero_ficticio': pregunta.dinero_ficticio
                        })
                        operacion_user.send_notificacion()
                        mensaje = 'Felicidades, has ganado $' + str(pregunta.dinero_ficticio)
                    else:
                        mensaje = 'Respuesta incorrecta, Gracias por participar'
        else:
            mensaje = 'La pregunta no está activa y no puedes responderla'
        return JsonResponse(
            state=STATES['SUCCESS'],
            message=mensaje
        )

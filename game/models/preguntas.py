from datetime import datetime, timedelta
import logging
from odoo import models, fields, api
import random
from odoo.exceptions import ValidationError,UserError
import pytz
_logger = logging.getLogger(__name__)

class PreguntaGame(models.Model):
    _name = 'oohel.pregunta_game'
    _description = 'Actividad - Game'

    pregunta = fields.Char(
        string='Pregunta',
    )
    respuesta = fields.Char(
        string='Respuesta'
    )
    active = fields.Boolean(
        string='Activa',
        default=True
    )
    activo = fields.Boolean(
        string='Activo',
        default=False
    )
    dinero_ficticio = fields.Integer(
        string='Dinero ficticio',
        default=0.0
    )
    participacion_ids = fields.One2many(
        comodel_name='oohel.participacion_game',
        inverse_name='pregunta_id',
        string='Operaciones'
    )



    def send_preguntas_game_to_users(self,accion):
        """"""
        user_tz = self.env.user.tz or 'America/Mexico_City'
        local = pytz.timezone(user_tz)
        today =  pytz.utc.localize(datetime.today()).astimezone(local).strftime('%Y-%m-%d %H:%M:%S')
        fecha_inicio = '2023-12-21 09:00:00'
        fecha_fin = '2023-12-21 18:59:59'

        if today>= fecha_inicio and today<= fecha_fin:
            preguntas_activas = self.env['oohel.pregunta_game'].search([('activo', '=', True)])
            if preguntas_activas:
                preguntas_activas.write({
                    'active': False
                })
            preguntas_sin_activar = self.env['oohel.pregunta_game'].search([('activo', '=', False)])
            tiempos=[30,35,40,45,50,55,60]
            # tiempos = [1,2,4,3]
            minutos = random.choice(tiempos)
            proxima_ejecucion = datetime.now() + timedelta(minutes=minutos)
            if accion == 'accion_uno':
                accion_planificada = self.env.ref('game.send_oohel_pregunta_game_to_users_accion_dos')
            if accion == 'accion_dos':
                accion_planificada = self.env.ref('game.send_oohel_pregunta_game_to_users_accion_uno')
            if accion_planificada:
                accion_planificada.sudo().write({
                    'active': True,
                    'numbercall': 1,
                    'nextcall': proxima_ejecucion
                })
            if len(preguntas_sin_activar) == 0:
                _logger.info('No existen preguntas por enviar, Registre preguntas para seguir participando.')
            else:
                pregunta_aleatoria_id = random.choice(preguntas_sin_activar.ids)
                pregunta_aleatoria = self.env['oohel.pregunta_game'].browse(pregunta_aleatoria_id)
                pregunta_aleatoria.write({
                    'activo': True
                })
                users = self.env['res.users'].sudo().search([('participante_x', '=', True)])

                title = "Actividad de preguntas rapidas activa, ganan los primeros 5 lugares"
                message = f'Se ha activado la pregunta rapida {pregunta_aleatoria.pregunta} para ganar ${pregunta_aleatoria.dinero_ficticio} pesos ficticios, !!Suerte!!.'
                model_notifications_push = self.env['oohel.notification_push']
                if users:
                    try:
                        request = model_notifications_push.send_notifications_to_users(['user'], users.ids, title,
                                                                                       message, 'game')
                        return request
                    except Exception as e:
                        print(e)




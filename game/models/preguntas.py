import datetime
import logging
from odoo import models, fields, api
import random


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

    def send_notificacion(self):
        users = self.env['res.users'].search([('participante_x', '=', True)])
        for user_id in users:
            title = "Actividad de preguntas rapidas activa, ganan los primeros 5 lugares"
            message = f'Estimado {user_id.name}, se ha actividad la pregunta rapida {self.pregunta} para ganar ${self.dinero_ficticio} pesos ficticios, !!Suerte!!.',
            model_notifications_push = self.env['oohel.notification_push']
            if user_id:
                try:
                    request = model_notifications_push.send_notifications_to_users(['user'], user_id.ids, title, message, 'game')
                    return request
                except Exception as e:
                    print(e)

    def send_preguntas_game_to_users(self):
        """"""
        today = fields.Datetime.now()
        fecha_inicio = datetime.datetime.strptime('2023-12-20 09:00:00', '%Y-%m-%d %H:%M:%S')
        fecha_fin = datetime.datetime.strptime('2023-12-20 18:59:59', '%Y-%m-%d %H:%M:%S')
        if today.date() == fecha_inicio.date() and today.time() >= fecha_inicio.time() and today.time() <= fecha_fin.time():
            preguntas_activas = self.env['oohel.pregunta_game'].search([('activo', '=', True)])
            preguntas_activas.write({
                'active': False
            })
            preguntas_sin_activar = self.env['oohel.pregunta_game'].search([('activo', '=', False)])
            pregunta_aleatoria = random.choice(preguntas_sin_activar)
            pregunta_aleatoria.write({
                'activo': True
            })
            pregunta_aleatoria.send_notificacion()
            accion_planificada = self.env.ref('game.send_oohel_pregunta_game_to_users')
            if accion_planificada:
                pass
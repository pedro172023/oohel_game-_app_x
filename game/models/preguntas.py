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
    participacion_ids = fields.One2many(
        comodel_name='oohel.participacion_game',
        inverse_name='pregunta_id',
        string='Operaciones'
    )

    def send_preguntas_game_to_users(self):
        """"""
        today = fields.Datetime.now()
        fecha_inicio = datetime.datetime.strptime('2023-12-20 09:00:00', '%Y-%m-%d %H:%M:%S')
        fecha_fin = datetime.datetime.strptime('2023-12-20 18:59:59', '%Y-%m-%d %H:%M:%S')
        if today.date() == fecha_inicio.date() and today.time() >= fecha_inicio.time() and today.time() <= fecha_fin.time():
            preguntas_activas = self.env['oohel.pregunta_game'].search([('active', '=', True)])
            pregunta_aleatoria = random.choice(preguntas_activas)
            pregunta_aleatoria.write({
                'activo': True
            })
            accion_planificada = self.env.ref('game.send_oohel_pregunta_game_to_users')
            if accion_planificada:
                pass

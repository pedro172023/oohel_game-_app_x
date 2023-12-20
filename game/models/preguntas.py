
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
    active= fields.Boolean(
        string='Activa',
        default=True
    )
    activo = fields.Boolean(
        string = 'Activo',
        default=False
    )
    participacion_ids = fields.One2many(
        comodel_name='oohel.participacion_game',
        inverse_name='pregunta_id',
        string='Operaciones'
    )

    def send_preguntas_game_to_users(self):
        """"""
        preguntas_activas=self.env['oohel.pregunta_game'].search([('active','=',True)])
        pregunta_aleatoria = random.choice(preguntas_activas)

        print('--------------------------pregunta_aleatoria')
        print(pregunta_aleatoria)
        today=fields.Datetime.now()








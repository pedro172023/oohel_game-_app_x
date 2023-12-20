
import logging
from odoo import models, fields, api


class Participaciones(models.Model):
    _name = 'oohel.participacion_game'
    _description = 'Participaciones - Game'

    user_id= fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )
    pregunta_id= fields.Many2one(
        comodel_name='oohel.pregunta_game',
        string='Pregunta'
    )
    respuesta= fields.Char(
        string='Respuesta'
    )
    correcta = fields.Boolean(
        string='¿Es una respuesta correcta?',
        default=False
    )
    puntos = fields.Char(

    )
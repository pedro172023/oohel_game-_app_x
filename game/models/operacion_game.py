"""
@author:
@date: 19/12/23
@name: operacion_game
"""
import logging
from odoo import models, fields, api


class OperacionGame(models.Model):
    _name = 'oohel.operacion_game'
    _description = 'Operaciones - Game'

    titulo = fields.Text(
        string='Actividad',
    )
    dinero_ficticio = fields.Float(
        string='Dinero ficticio',
        default=0.0
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario',
    )

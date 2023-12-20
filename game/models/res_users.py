"""
@author:
@date: 19/12/23
@name: operacion_game
"""
import logging
from odoo import models, fields, api

class ResUsers(models.Model):
    """"""
    _inherit='res.users'

    participante_x = fields.Boolean(
        string='Participante X',
    )

    saldo = fields.Float(
        string='Saldo',
    )

    operacion_ids = fields.One2many(
        comodel_name='oohel.operacion_game',
        inverse_name='user_id',
        string='Operaciones game'
    )

    def get_saldo(self):
        """Suma de las operaciones del usuario."""
        return sum(self.operacion_ids.mapped('dinero_ficticio'))

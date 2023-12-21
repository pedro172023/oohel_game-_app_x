"""
@author:
@date: 19/12/23
@name: operacion_game
"""
import logging
from odoo import models, fields, api
import base64


class ResUsers(models.Model):
    """"""
    _inherit = 'res.users'

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
        dinero_ficticio_por_operacion = sum(self.operacion_ids.mapped('dinero_ficticio'))
        cantidad_premios = sum(
            self.env['oohel.premio'].search([('user_id', '=', self.id)]).mapped('puja_maxima_empleado'))
        total = dinero_ficticio_por_operacion - cantidad_premios
        return total

    def get_premios(self):
        premios = []
        premios_rq = self.env['oohel.premio'].search([])
        for premio in premios_rq:
            imagen_b64 = ''
            if premio.image:
                imagen_b64 = str(premio.image)
                imagen_b64 = imagen_b64.replace("b'", '')
                imagen_b64 = imagen_b64.replace(imagen_b64[len(imagen_b64) - 1], "")
            premios.append({
                'image': imagen_b64,
                'premio': premio.premio,
                'minimo_puja': premio.minimo_puja,
                'maximo_puja': premio.maximo_puja,
                'ganador': premio.user_id.name if premio.user_id else 'Aun sin ganador',
                'puedo_pujar': self.get_saldo() >= premio.minimo_puja
            })
        return premios

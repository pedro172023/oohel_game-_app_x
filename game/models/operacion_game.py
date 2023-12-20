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
        required=True
    )
    dinero_ficticio = fields.Integer(
        string='Dinero ficticio',
        default=0
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario',
        required=True
    )

    def send_notificacion(self):
        title = "Has ganado " + str(self.dinero_ficticio) + " pesos ficticios"
        message = f'Estimado {self.user_id.name} se te ha otorgado {self.dinero_ficticio} pesos ficticios, por la actividad {self.titulo}'
        model_notifications_push = self.env['oohel.notification_push']
        if self.user_id:
            try:
                request = model_notifications_push.send_notifications_to_users(['user'], self.user_id.ids, title, message, 'game')
                return request
            except Exception as e:
                print(e)

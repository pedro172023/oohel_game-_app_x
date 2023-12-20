import logging
from odoo import models, fields, api


class Participaciones(models.Model):
    _name = 'oohel.participacion_game'
    _description = 'Participaciones - Game'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )
    pregunta_id = fields.Many2one(
        comodel_name='oohel.pregunta_game',
        string='Pregunta'
    )
    respuesta = fields.Char(
        string='Respuesta'
    )
    correcta = fields.Boolean(
        string='¿Es una respuesta correcta?',
        default=False
    )

    def send_notificacion(self):
        title = "Puntos por participar en las preguntas rapidas"
        message = f'Estimado {self.user_id.name}, se le ha premiado con ${self.pregunta_id.dinero_ficticio} pesos ficticios por contestar la pregunta {self.pregunta_id.pregunta} correctamente.',
        model_notifications_push = self.env['oohel.notification_push']
        if self.user_id:
            try:
                request = model_notifications_push.send_notifications_to_users(['user'], self.user_id.ids, title,
                                                                               message, 'game')
                return request
            except Exception as e:
                print(e)

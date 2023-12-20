# @Author: pedro172023
# -*- coding: utf-8 -*-
from odoo import api, fields, models

res_models_notifications = []
from odoo.addons.oohel_notification_push.models.notification_push import TIPO_APP


class SegmentoNotificationPush(models.Model):
    _name = 'oohel.segmento_notification_push'
    _description = 'Oohel/Segmentos notificaciones push'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    res_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo relacionado',
        domain=lambda self: self.domain_res_models_notifications(),
        ondelete='cascade',
        required=True
    )

    app = fields.Selection(
        selection=TIPO_APP,
        string='App',
    )

    def domain_res_models_notifications(self):
        return [('model','in', res_models_notifications)]
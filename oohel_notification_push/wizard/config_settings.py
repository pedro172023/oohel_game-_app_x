# -*- coding: utf-8 -*-
from odoo import api, fields, models


class NotificationPushConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    clave_server_fcm = fields.Char(string="Clave del servidor")
    url_send_fcm = fields.Char(string="Url de envio")

    @api.model
    def set_values(self):
        super(NotificationPushConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("oohel.clave_server_fcm", self.clave_server_fcm)
        self.env['ir.config_parameter'].sudo().set_param("oohel.url_send_fcm", self.url_send_fcm)

    @api.model
    def get_values(self):
        notification_push = super(NotificationPushConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        clave_server_fcm = params.get_param('oohel.clave_server_fcm', default=False)
        url_send_fcm = params.get_param('oohel.url_send_fcm', default=False)
        notification_push.update(
            clave_server_fcm=clave_server_fcm,
            url_send_fcm=url_send_fcm,
        )
        return notification_push

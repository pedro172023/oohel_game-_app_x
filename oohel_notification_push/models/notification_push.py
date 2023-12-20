"""
@author pedro172023
"""

# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request, route
import requests
import json
TIPO_APP = [
    ('game', 'App Game')
]


class NotificacionesPush(models.Model):
    _name = 'oohel.notification_push'
    _rec_name = "token"
    _description = 'Oohel/Notificaciones push'

    token = fields.Text(
        string="Token"
    )

    res_model = fields.Char(
        'Modelo de documento relacionado',
        index=True
    )

    res_id = fields.Integer(
        string='ID del documento relacionado',
        index=True
    )

    app = fields.Selection(
        selection=TIPO_APP,
        string='App',
    )

    def send_notifications_to_users(self, res_models=False, res_ids=False, title_message=False, body_message=False, app=False):
        """
        Args:
            res_models:
            res_ids:
            title_message:
            body_message:

        Returns:
            Estado del envio
        """
        domain_search = []
        usuario = self.env.user.id
        if res_models and title_message and body_message:
            for i in range(len(res_models)):
                res_models[i] = self.get_res_model(res_models[i])
            domain_search.append(('res_model', 'in', res_models))
            domain_search.append(('app', '=', app))
            if res_ids and len(res_models) == 1:
                domain_search.append(('res_id', 'in', res_ids))
                users = self.env[res_models[0]].sudo().search([('id', 'in', res_ids)])
                for user in users:
                    self.env['oohel.user_notification_push'].sudo().create({
                        'res_model': res_models[0],
                        'res_id': user.id,
                        'title': title_message,
                        'message': body_message,
                        'app': app
                    })
            request_tokens = self.env['oohel.notification_push'].sudo().search(domain_search)
            if request_tokens:
                tokens = [record.token for record in request_tokens if record.token]
                return self.send_notification_to_tokens(tokens, title_message, body_message)
            else:
                raise ValidationError('Los registros seleccionados no estan dados de alta para recibir notificaciones')
        else:
            raise ValidationError('Es necesario incluir a que segmento se enviara la notificacíon')
        return False

    def send_notification_to_tokens(self, tokens_notification, title, body):
        """
        {
            "multicast_id": id del multicast "success": cuantas notificaciones
            se enviaron "failure": cuantas notificaciones fallaron
            "canonical_ids":0, "results":[
                    {"message_id": id del mensaje}
                ]
        }
        Args:
            tokens_notification:
            title:
            body:
        Returns:
            Respuesta del envio, objecto
        """
        url = self.env['ir.config_parameter'].sudo().get_param('oohel.url_send_fcm', False)
        clave_server_fcm = self.env['ir.config_parameter'].sudo().get_param('oohel.clave_server_fcm', False)
        if url and clave_server_fcm:
            msg = {
                'notification': {
                    "title": title,
                    "body": body,
                },
                "registration_ids": tokens_notification
            }
            headers = {
                'Authorization': 'key=' + clave_server_fcm,
                'Content-Type': 'application/json'}
            r = requests.post(url, data=json.dumps(msg), headers=headers)
            return str(r.content, 'utf-8')
        else:
            raise ValidationError(
                'La url de envio y la clave de servidor de Firebase Cloud Messaging deben de estar configurados')

    def validate_token_notification(self, res_model, token_notification, res_id_current, app):
        """
        Args:
            res_model:
            token_notification:
            res_id_current:
        """
        model_notifications_push = self.env['oohel.notification_push']
        res_model = self.get_res_model(res_model)
        request_verify_token_notification = model_notifications_push.sudo().search(
            [('token', '=', token_notification), ('res_model', '=', res_model), ('app', '=', app)])
        if request_verify_token_notification:
            user_current_token = request_verify_token_notification.res_id
            if user_current_token != res_id_current:
                update_user_token = request_verify_token_notification.sudo().write({
                    'res_id': res_id_current,
                    'res_model': res_model,
                    'app': app
                })
                if update_user_token:
                    return 200, "Todo bien"
                else:
                    return 500, "Todo mal"
            else:
                return 200, "Todo bien"
        else:
            token_notification_create = model_notifications_push.sudo().create({
                'res_id': res_id_current,
                'token': token_notification,
                'res_model': res_model,
                'app': app
            })
            if token_notification_create:
                return 200, "Todo bien"
            else:
                return 500, "Todo mal"

    def destroy_token_notification(self, token_notification):
        """
        Args:
            token_notification:
        """
        model_notifications_push = self.env['oohel.notification_push']
        request_destroy_token_notification = model_notifications_push.sudo().search(
            [('token', '=', token_notification)])
        if request_destroy_token_notification:
            request_destroy_token_notification.sudo().unlink()
            return 200, "Todo bien"
        return 500, "Todo mal"

    def power_on_remove_tokens_expired(self):
        clave_server_fcm = self.env['ir.config_parameter'].sudo().get_param('oohel.clave_server_fcm', False)
        tokens_notificacion_push_request = self.env['oohel.notification_push'].sudo().search([])
        headers = {
            'Authorization': 'key=' + clave_server_fcm,
            'Content-Type': 'application/json'
        }
        for token_notification in tokens_notificacion_push_request:
            validate_token = requests.post('https://iid.googleapis.com/iid/info/' + token_notification.token, data='',
                                           headers=headers)
            if 'error' in validate_token.json():
                token_notification.sudo().unlink()

    def get_res_model(self, res_model):
        """
        Args:
            res_model:
        """
        res_model_parser = res_model
        if not 'oohel.' in res_model_parser:
            if res_model_parser == 'user' or res_model_parser == 'users':
                res_model_parser = 'res.users'
            else:
                res_model_parser = 'oohel.' + res_model_parser
        return res_model_parser
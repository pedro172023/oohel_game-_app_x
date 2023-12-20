"""
@author pedro172023 |
"""
# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

try:
    from odoo.addons.core.libs.response import valid_token, makeResponse, STATES
except ImportError as ee:
    _logger.error("Error al importar el modulo de post_covid_libs, por favor revise el path")


class NotificationPush(http.Controller):
    @http.route('/api/v1/notification_push/add', method=['POST'], type='http', auth='none', csrf=False, cors='*')
    @valid_token
    def notification_push_add(self, **post):
        res_id_current = post['token']['usuario_id']
        token_notification = post.get('token_notification', False)
        res_model = post.get('res_model', False)
        app = post.get('app', False)
        model_notifications_push = http.request.env['oohel.notification_push']
        if token_notification and res_model and res_id_current:
            state, message = model_notifications_push.validate_token_notification(res_model, token_notification, res_id_current.id, app)
            return makeResponse(state, message=message)
        return makeResponse(500, message="Todo mal")

    @http.route('/api/v1/notification_push/destroy', method=['POST'], type='http', auth='none', csrf=False, cors='*')
    def notification_push_destroy(self, **post):
        token_notification = post.get('token_notification', False)
        model_notifications_push = http.request.env['oohel.notification_push']
        if token_notification:
            state, message = model_notifications_push.destroy_token_notification(token_notification)
            return makeResponse(state, message=message)
        return makeResponse(500, message="Todo mal")

    @http.route('/api/v1/notification_push/user', method=['POST'], type='http', auth='none', csrf=False, cors='*')
    @valid_token
    def notifications_push_user(self, **post):
        type_user = post.get('ttype', False)
        app = post.get('app', False)
        id_user = post['token']['usuario_id']
        if type_user and id_user:
            request_notificaciones = request.env['oohel.user_notification_push'].getMessagesUser(app, type_user, id_user.id)
            return makeResponse(200, message="Todo bien", data=request_notificaciones)
        return makeResponse(500, message="Todo mal")
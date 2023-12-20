"""
@author pedro172023
@name user_notification_push.py
"""
from odoo import api, fields, models
from odoo.addons.oohel_notification_push.models.notification_push import TIPO_APP


class UserNotificationPush(models.Model):
    _name = 'oohel.user_notification_push'
    _description = 'Notification user'
    _order = 'create_date desc'

    res_model = fields.Char(
        'Modelo de documento relacionado',
        index=True
    )

    res_id = fields.Integer(
        string='ID del documento relacionado',
        index=True
    )

    title = fields.Char(
        string="Titulo"
    )

    message = fields.Text(
        string="Mensaje"
    )

    app = fields.Selection(
        selection=TIPO_APP,
        string='App',
    )


    def getMessagesUser(self, app, type_user, res_id):
        messsage_request = []
        type_user = self.env['oohel.notification_push'].sudo().get_res_model(type_user)
        if type_user and res_id:
            messsage_request = self.env['oohel.user_notification_push'].sudo().search_read(
                [('res_model', '=', type_user), ('app', '=', app), ('res_id', '=', res_id)],
                [
                    'title',
                    'message',
                    'create_date',
                ], limit=15
            )
        messsage_request = list(map(lambda item: self.parserItemFecha(item), messsage_request))
        return messsage_request

    def parserItemFecha(self, item):
        """
        Args:
            item:
        """
        item['create_date'] = fields.Date.to_string(item['create_date'])
        return item

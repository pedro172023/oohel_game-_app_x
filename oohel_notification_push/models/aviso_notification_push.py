# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from odoo.addons.oohel_notification_push.models.notification_push import TIPO_APP


class AvisosNotificationPush(models.Model):
    """
    Clase para los avisos con notificaciones push dirigidos a segmentos de usuarios, esto sirve para una implementacion
    posterior.
    """
    _name = 'oohel.aviso_notification_push'
    _order = 'fecha_publicacion desc'
    _description = 'Oohel/Avisos con notificaciones push'

    name = fields.Char(
        string="Título",
        required=True,
    )

    descripcion = fields.Text(
        string="Descripcion",
        required=True,
    )

    dirigido_users = fields.Many2many(
        'oohel.segmento_notification_push',
        string="Dirigido A",
        required=True,
        relation="oohel_segmento_aviso_notification_push"
    )

    fecha_publicacion = fields.Date(
        string="Fecha de Publicacion:",
        default=fields.Date.today()
    )

    app = fields.Selection(
        selection=TIPO_APP,
        string='App',
    )

    visible = fields.Selection(
        [
            ('1', 'Borrador'),
            ('2', 'Publicado')
        ],
        default='1',
        required=True,
    )

    @api.onchange('visible','fecha_publicacion')
    def onchange_visisble(self):
        for record in self:
            if record.visible == '2':
                fecha_publicacion = fields.Datetime.from_string(record.fecha_publicacion)
                if fecha_publicacion > datetime.now():
                    raise UserError('La fecha de publicación debe ser menor o igual a la fecha de hoy')

    def send_notification_aviso(self):
        model_notifications_push = self.env['oohel.notification_push']
        segmentos = []
        if self.dirigido_users:
            for segmento in self.dirigido_users:
                segmentos.append(segmento.res_model_id.model)
            try:
                resquest = model_notifications_push.send_notifications_to_users(segmentos, False, self.name, self.descripcion)
                return resquest
            except Exception as e:
                raise UserError(str(e))
        else:
            raise UserError('Este aviso no esta dirigido a alguien, favor de revisar')

    def getAvisos(self, type_user, app):
        """
        Args:
            type_user:
        """
        type_user = self.env['oohel.notification_push'].sudo().get_res_model(type_user)
        avisos_request = self.env['oohel.aviso_notification_push'].sudo().search_read(
            [('dirigido_users.res_model_id.model','=',type_user), ('visible', '=', '2'), ('app', '=', app)],
            [
                'name',
                'descripcion',
                'fecha_publicacion',
            ], limit=15
        )
        avisos_request = list(map(lambda item: self.parserItemFecha(item), avisos_request))
        return avisos_request

    def parserItemFecha(self, item):
        """
        Args:
            item:
        """
        item['fecha_publicacion'] = fields.Date.to_string(item['fecha_publicacion'])
        return item
"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 11/05/21
@name: settings.py
"""
from odoo import models, fields, api


class SettingsCore(models.TransientModel):
    """Modelo de configuración para core
    Attributes:
        url_core_server  URL del servidor de core.
        secret_key   Llave de encriptación se usa para validar tokens de las interfaces
        days_active_token  Duración en días de los los tokens.
    """
    _inherit = 'res.config.settings'

    days_active_token = fields.Integer(
        string='Duración del token (días)',
    )

    def set_values(self):
        """
        Actualizar los parámetros del sistema.
        :return:
        """

        super(SettingsCore, self).set_values()
        IrConfig = self.env['ir.config_parameter'].sudo()
        IrConfig.set_param('core.days_active_token', int(self.days_active_token))

    @api.model
    def get_values(self):
        """
        Obtener los parámetros del sistema y mostrar en la configuración
        :return:
        """
        res = super(SettingsCore, self).get_values()
        IrConfig = self.env['ir.config_parameter'].sudo()
        res.update({
            'days_active_token': IrConfig.get_param('core.days_active_token', 30),
        })

        return res

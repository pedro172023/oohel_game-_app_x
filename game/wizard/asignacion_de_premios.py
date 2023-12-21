from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, ValidationError


class WizardAsignarPremios(models.TransientModel):
    _name = 'oohel.wizard_asignar_premios'
    _description = 'Wizard - Asignar Premios'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Empleado',
    )

    premio_id = fields.Many2one(
        comodel_name='oohel.premio',
        string='Premio',
    )

    puja_maxima_empleado = fields.Integer(
        string='Puja máxima - Empleado',
        default=0
    )

    def asignar(self):
        """"""
        if self.user_id:
            title = "Has ganado el premio " + str(self.premio_id.premio)
            message = f'Estimado {self.user_id.name} has ganado el premio {self.premio_id.premio} con una puja máxima de ${self.puja_maxima_empleado}\n'
            saldo_empleado = self.user_id.get_saldo()
            if self.puja_maxima_empleado >= saldo_empleado:
                message += f'Tendras que dar a la empresa la cantidad de ${self.puja_maxima_empleado - saldo_empleado} en dinero real.'
            else:
                message += f'Has ganado el premio con ${self.puja_maxima_empleado} dinero ficticio, aún cuentas con ${saldo_empleado - self.puja_maxima_empleado} dinero ficticio.'
            model_notifications_push = self.env['oohel.notification_push']
            self.premio_id.sudo().write({
                'user_id': self.user_id.id,
                'puja_maxima_empleado': self.puja_maxima_empleado
            })
            if self.user_id:
                try:
                    request = model_notifications_push.send_notifications_to_users(['user'], self.user_id.ids, title,
                                                                                   message, 'game')
                    return request
                except Exception as e:
                    print(e)

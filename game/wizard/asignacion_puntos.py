from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, ValidationError


class WizardHAsignarPuntos(models.TransientModel):
    _name = 'oohel.wizard_asignar_puntos'
    _description = 'Wizard - Asignar Puntos'

    user_ids = fields.Many2many(
        'res.users',
        string='Parcipantes',
    )

    titulo = fields.Text(
        string='Actividad',
    )

    dinero_ficticio = fields.Integer(
        string='Dinero ficticio',
        default=0.0
    )

    def asignar(self):
        if len(self.user_ids) == 0:
            raise ValidationError("Debe seleccionar al menos un participante")
        if self.dinero_ficticio == 0:
            raise ValidationError("No se puede asignar 0 pesos ficticios")
        for user in self.user_ids:
            operacion = self.env['oohel.operacion_game'].create({
                'user_id': user.id,
                'titulo': self.titulo,
                'dinero_ficticio': self.dinero_ficticio
            })
            operacion.send_notificacion()
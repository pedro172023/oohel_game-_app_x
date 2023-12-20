from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, ValidationError


class WizardRegistrarPregunta(models.TransientModel):
    _name = 'oohel.wizard_registrar_pregunta'
    _description = 'Wizard - Registrar Pregunta'

    pregunta = fields.Char(
        string='Pregunta',
    )
    respuesta = fields.Char(
        string='Respuesta'
    )

    def registrar_pregunta(self):
        if not self.pregunta:
            raise ValidationError('La pregunta debe tener un título.')
        if not self.respuesta:
            raise ValidationError('La pregunta debe tener un respuesta.')
        self.env['oohel.pregunta_game'].create({
            'pregunta': self.pregunta,
            'respuesta': self.respuesta,
        })
import logging
from odoo import models, fields, api


class OohelPremio(models.Model):
    _name = 'oohel.premio'
    _description = 'Oohel - Premio'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Ganador'
    )
    premio = fields.Char(
        string='Premio'
    )
    minimo_puja = fields.Integer(
        string='Mínimo de puja',
        default=100
    )
    maximo_puja = fields.Integer(
        string='Puja máxima',
        default=1600
    )

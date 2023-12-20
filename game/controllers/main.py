"""
@autor: Pedro Sánchez H. <pedro.sanchez@oohel.net>
@date: 19/12/2023
@name: main.py
"""
import logging
from odoo.addons.core.libs.response import valid_token, makeResponse, STATES, badRequest, JsonResponse
from odoo.http import route, request, Controller
logger = logging.getLogger(__name__)


class MainControllerCoreApp(Controller):
    """
        Controlador principal para la app
    """
    @route('/api/v1/saldo', method=['GET'], cors='*', csrf=False, auth="none", type="http", website=False)
    @valid_token
    def get_saldo(self, **post):
        user = post['token']['usuario_id']
        saldo = user.get_saldo()
        return makeResponse(
            state=STATES['SUCCESS'],
            message='Saldo',
            data=saldo,
        )
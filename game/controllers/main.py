"""
@author: Miguel Cabrera Ramírez <miguel.cabrera@oohel.net><mdark1001>
@project: 
@date: 00/00/2023
"""
import base64
import logging
from distutils.util import strtobool
from odoo.fields import Datetime
from odoo.addons.core.libs.response import valid_token, makeResponse, STATES, badRequest, JsonResponse
from odoo.http import route, request, Controller
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
from pytz import timezone, UTC


class MainControllerCoreApp(Controller):
    """
        Controlador principal para la aplciación de mantenimiento
    """

    @route('/api/v1/saldo', method=['GET'],
           cors='*',
           csrf=False,
           auth="none", type="http",
           website=False)
    @valid_token
    def get_saldo(self, **post):
        user = post['token']['usuario_id']
        # request.env
        mntn = request.env['res.users'].with_context(lang='es_MX').with_user(user)
        return makeResponse(
            state=STATES['SUCCESS'],
            message='Saldo',
            data=mntn,
        )


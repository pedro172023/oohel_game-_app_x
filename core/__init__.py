"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 28/04/21
@name: __init__.py
"""

from . import models
from . import controllers
from . import wizards
from odoo import api
from odoo.api import SUPERUSER_ID


def post_init_hook(cr, registry):
    """
    Registrar usuario de interfaces después de instalar el módulo.
    :param cr: Cursor
    :param registry:
    :return: Boolean()
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    return True

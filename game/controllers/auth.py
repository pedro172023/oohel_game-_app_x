"""
@author: Miguel Cabrera Ramírez <miguel.cabrera@oohel.net><mdark1001>
@project: 
@date: 00/00/2023

"""
import re
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.core.controllers import auth

VALIDATOR = r"^[0-9]+$"


class AuthGame(auth.AuthCoreService):

    def is_valid_email(self, email):
        result = super(AuthGame, self).is_valid_email(email)
        return True

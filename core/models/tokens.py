"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 03/05/21
@name: tokens
"""
import logging
from odoo import models, fields, api, http
from datetime import datetime, timedelta, date
from odoo.http import request

_logger = logging.getLogger(__name__)
try:
    import jwt
except ImportError:
    _logger.info("Error al importar JWT, intenta con: pip3 install PyJWT")


class Tokens(models.Model):
    """  Tokens de accesos para las interfaces """
    _name = 'core.tokens'
    _inherit = ['mail.thread']
    _description = 'Tokens de acceso para el usuario de interfaces '
    _rec_name = 'usuario_id'

    usuario_id = fields.Many2one(
        'res.users',
        string='Usuario',
        required=True
    )
    token = fields.Char(
        string='Token',
        required=True,
    )
    fecha_login = fields.Datetime(
        string='Fecha de inicio de sesión',
        default=fields.Datetime.now(),
    )
    fecha_expiracion = fields.Date(
        string='Fecha de expiración',
        required=True,
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )

    is_expired = fields.Boolean(
        compute="check_token_is_expired",
        string='Token Expirado',
    )
    ip_address = fields.Char(
        string='IP',
        required=True,
    )

    @api.depends('fecha_expiracion')
    def check_token_is_expired(self):
        """
        :return:
        """
        for record in self:
            record.is_expired = date.today() > record.fecha_expiracion

    def get_secret_key(self):
        """
        :return:
        """
        return self.env['ir.config_parameter'].sudo().get_param('core.secret_key', '')

    def get_days_active_token(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('core.days_active_token'))

    def get_usuario_by_toke(self, token):
        _token = self.search(
            [
                ('token', '=', token),
            ], limit=1)
        if _token.exists():
            if _token.is_expired:
                _token.sudo().write({'active': False})  # Token expirado lo archivamos
                return False
            return _token
        return False

    def create_token(self, user, ip_address):
        """
        Args:
            user:
        """
        try:
            exp = datetime.utcnow() + timedelta(days=self.get_days_active_token())
            payload = {
                'exp': exp,
                'iat': datetime.utcnow(),
                'sub': user.get('uid'),
                'id': user.get('uid'),
                'lgn': user.get('login'),
            }

            token = jwt.encode(
                payload,
                self.get_secret_key(),
                algorithm='HS256'
            )
            self.save_token(token, user.get('uid'), exp, ip_address)

            return token.decode('utf-8')
        except Exception as ex:
            _logger.error(ex)
            raise

    def save_token(self, token, usuario_id, exp, ip_address):
        """
        Args:
            token:
            user_id:
            exp:
        """
        self.sudo().create({
            'usuario_id': usuario_id,
            'token': token,
            'fecha_expiracion': exp,
            'create_uid': usuario_id,
            'ip_address': ip_address
        })

    def verify(self, token):
        """
        Args:
            token:
        """
        record = self.env['core.tokens'].sudo().search([
            ('token', '=', token)
        ], limit=1)

        if not record.exists():
            _logger.info('not found %s' % token)
            return False
        if record.is_expired:
            return False
        return record.usuario_id

    def verify_token(self, token):
        """
        :param:
            token: Json Web token,
        :return: Dict(status=Boolean,message=String)
        """
        result = {
            'status': False,
            'message': None,
            'code': 400
        }
        try:
            payload = jwt.decode(token, self.get_secret_key(), algorithms='HS256')
            token_valido = self.verify(token)
            if not token_valido:
                result['message'] = 'El token no es valido o ya expiró'
                result['code'] = 404
                return result
            if token_valido.id != payload['id']:
                result['message'] = 'El token no conicide con el usuario'
                result['code'] = 404
                return result
            result['status'] = True
            result['usuario_id'] = token_valido
            result['payload'] = payload
            result['code'] = 200
            return result
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
            result['code'] = 404
            result['message'] = 'Token no valido'
            return result

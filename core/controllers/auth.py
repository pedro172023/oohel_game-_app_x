"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 03/05/21
@name: auth
"""
import logging
from odoo.http import Controller, route, request
from odoo.addons.core.libs.response import makeResponse, badRequest, incorrectToken, validate_token, STATES

try:
    from validate_email import validate_email
except ImportError:
    raise ImportError(
        'install with pip3 install validate_email')

_logger = logging.getLogger(__name__)


class AuthCoreervice(Controller):
    """ Autenticación de usuarios de interfaces """

    @route('/api/v1/login/', method=['POST'], cors='*', csrf=False, auth="none", type="http", website=False)
    def login(self, **post):
        """
        Endpoint para realizar login de usuarios de interfaces, Si el login es exitoso retorno
        un json con la llave 'token' usando la librería JWT usando una llave de cifrado
        por cada entorno (Desarrollo,QA,Productivo).
        El json contiene una llave 'message' que devuelve el mensaje de error especifico.
        Ejemplo de la respuesta si es exitoso:

         {
            "message": "Login",
            "data": {
                "data": {
                    "email": "interfaces@core.com",
                    "uid": 391,
                    "login": "interfaces@core.com",
                    "context": {
                        "lang": "es_MX",
                        "tz": "America/Mexico_City",
                        "uid": 391
                    }
                },
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjI3MzQ2MzQsIml..."
            }
        }
        Si es incorrecto los accesos:
        <code>
            {
                "message": "Email o Contraseña incorrectos",
                "data": {}
            }
        </code>
        :param:
            **post:Dict()
        :return:
            Response<200,404,500>
        """
        email = post.get('email', False)
        password = post.get('password', False)

        result_auth = False
        if email and password:
            if self.is_valid_email(email):

                try:
                    result_auth = request.session.authenticate(request.session.db, email, password)
                    del post['password']
                    self.run_extra_validation(**post)
                except Exception as ee:
                    _logger.error(str(ee).encode('UTF-8'))
                    return makeResponse(state=STATES['NOT_FOUND'],
                                        message=str(ee))
                if not result_auth:
                    return makeResponse(state=STATES['NOT_FOUND'],
                                        message='Email o Contraseña incorrectos')
                if request.session.uid:
                    data = {
                        'email': email,
                        'uid': request.env.user.id,
                        'user': {
                            'name': request.env.user.name
                        },
                    }
                    if data:
                        data.update(request.session)
                        del data['session_token']
                        del data['db']
                        del data['debug']
                        del data['context']
                        del data['geoip']
                        ip_address = request.httprequest.environ['REMOTE_ADDR']
                        token = request.env['core.tokens'].create_token(data, ip_address)
                        return makeResponse(state=STATES['SUCCESS'],
                                            data={
                                                'data': data,
                                                'token': token
                                            },
                                            message="Login"
                                            )
                else:
                    return makeResponse(state=STATES['SERVER_ERROR'],
                                        message='Email o Contraseña incorrectos')
            else:
                return makeResponse(state=STATES['SERVER_ERROR'],
                                    message='El Email que ingresó no cumple con una estructura valida')
        return makeResponse(state=STATES['SERVER_ERROR'], message='El email y contraseña son requeridos')

    @route('/api/v1/test/', method=['POST'], cors='*', csrf=False, auth="none", type="http", website=False)
    def test_token_header(self, **post):
        """
        Test para validar el token de acceso después de hacer login en el sistema.
        :param post: Kwgars extra
        :return: Response<200,403,500>

        """
        token = validate_token()
        if token and token['status']:
            return makeResponse(STATES['SUCCESS'], {}, message='Token valido')
        return makeResponse(token['code'], message=token['message'])

    def is_valid_email(self, email):
        """
        Validar estructura de email.
        :param:
            email:String
        :return: Boolean
        """
        return validate_email(email)

    def run_extra_validation(self, **kwargs):
        pass

"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 03/05/21
@name: response
"""
import functools
import json
from odoo.http import request, Response
import logging

headers_response = [
    ("Access-Control-Allow-Origin", "*"),
    ('Content-Type', 'application/json'),
    ('Access-Control-Allow-Methods', "GET,POST,PUT,PATCH"),
    ("Access-Control-Allow-Credentials", "true"),
    ("Access-Control-Allow-Headers", "Authorization")
]
STATES = dict(
    BAD_REQUEST=400,
    UNAUTHORIZED=401,
    NOT_FOUND=404,
    SUCCESS=200,
    SUCCESS_CREATED=201,
    SERVER_ERROR=500,
    TOKEN_ERROR=403
)

_logger = logging.getLogger(__name__)


def makeResponse(state, data={}, message="Todo bien", ):
    """
    Crear respuestas a las peticiones http/https de manera simplificada usando la librería de odoo <Response>
    :param state: int(), Estatus HTTP <200,400,500>,
    :param data:  Dict(), Respuesta Json
    :param message: String(), Mensaje de respuesta.
    :return: Response()
    """
    payload = json.dumps({
        'message': message,
        'data': data,
    })
    _logger.info(message)
    _logger.info(data)
    return Response(payload, status=state, headers=headers_response)


def JsonResponse(state, data={}, message="Todo bien"):
    payload = json.dumps({
        'message': message,
        'data': data,
    })
    _logger.info(message)
    _logger.info(data)
    return Response(payload, status=state, headers=headers_response,mimetype='application/json')


def incorrectToken():
    """
    Método para devolver un response de token invalido o expirado.
    :return: Response(403,'Error, token invalido o expirado')
    """
    return makeResponse(STATES['TOKEN_ERROR'], message='Error, token invalido o expirado')


def badRequest():
    """
    Método para devolver una respuesta incorrecta.
    :return: Response(403,'Error al procesar su solicitud, por favor inténtelo más tarde')
    """
    return makeResponse(STATES['BAD_REQUEST'], message='Error al procesar su solicitud, por favor inténtelo más tarde')


def parse_request():
    """
    Parsea un request para obtener el token, headers, body de la petición.
    Se usa en la validación del token.
    :return: http_method, body, headers, token
    """
    http_method = request.httprequest.method
    try:
        body = request.params
    except Exception:
        body = {}

    headers = dict(list(request.httprequest.headers.items()))
    if 'wsgi.input' in headers:
        del headers['wsgi.input']
    if 'wsgi.errors' in headers:
        del headers['wsgi.errors']
    if 'HTTP_AUTHORIZATION' in headers:
        headers['Authorization'] = headers['HTTP_AUTHORIZATION']

    # extract token
    token = ''
    if 'Authorization' in headers:
        try:
            # Bearer token_string
            token = headers['Authorization'].split(' ')[1]
        except Exception:
            pass

    return http_method, body, headers, token


def validate_token():
    """
    En un request se invoca la validación dek token
    -  Sí en el request no existe el token retorna un False
    - Si existe el token se valida la fecha de expiración
    :return: Bool()
    """
    http_method, body, headers, token = parse_request()
    if not token:
        return False
    token_valid = request.env['core.tokens'].sudo().verify_token(token)

    return token_valid


def valid_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        http_method, body, headers, token = parse_request()
        if not token:
            return incorrectToken()
        token_valid = request.env['core.tokens'].sudo().verify_token(token)
        if not token_valid['status']:
            return incorrectToken()
        kwargs['token'] = token_valid
        return func(*args, **kwargs)
    return wrapper


def validate_required_items(fields, values):
    """
    Validar los campos de un diccionario que deben estar presentes y no ser nulos
    :param fields: Array()
    :param values: Dict()
    :return: Dict(valid=Bool(),message=Array())
    La propiedad message es una lista de los campos faltantes en el diccionario
    """
    result = {
        'valid': True,
        'message': [],
    }
    value_keys = values.keys()
    for item in fields:
        if not item in value_keys:
            result['message'].append("%s es requerido" % item)
            result['valid'] = False
        elif not values[item]:
            result['message'].append("%s es requerido" % item)
            result['valid'] = False
    return result

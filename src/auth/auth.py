import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-leticialourenco.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header
def get_token_auth_header():
    # get authorization part of the header from request
    header = request.headers.get('Authorization', None)
    if not header:
        raise AuthError({
            'status_code': 'authorization_header_missing',
            'error': 'Authorization header is expected.'
        }, 401)
    # separate content of authorization header in a list
    auth = header.split()
    # flag error in case token type is not bearer
    if auth[0] != 'Bearer':
        raise AuthError({
            'status_code': 'invalid_header',
            'error': 'Authorization header must start with "Bearer".'
        }, 401)
    # flag error in case token missing
    if not auth[1]:
        raise AuthError({
            'status_code': 'invalid_header',
            'error': 'Authorization header must contain a Bearer token.'
        }, 401)
    # return index 1 of auth that contain the bearer token value
    return auth[1]

def check_permissions(permission, payload):
    # check for missing permissions in the jwt decoded - payload
    if 'permissions' not in payload:
        raise AuthError({
            'status_code': 'invalid_claims',
            'error': 'Permissions not included in JWT.'
        }, 400)
    # if permissions list does not contain specific permission needed
    if permission not in payload['permissions']:
        raise AuthError({
            'status_code': 'unauthorized',
            'error': 'Permission not found.'
        }, 403)
    # return true in case permissions are checked with no errors
    return True

# decode jwt code wrote in a follow along exercise
# by Udacity FSND course on Authentication and Authorization
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # get requests header using jose jwt and passing the token as param
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # check for kid within the header to verify it's good to use
    if 'kid' not in unverified_header:
        raise AuthError({
            'status_code': 'invalid_header',
            'error': 'Authorization malformed.'
        }, 401)
    # populate rsa_key with values from header
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        # decode jwt passing the token param,
        # the previously obtained rsa key,
        # and project specific auth0 information
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        # raise an error if the signature is no longer valid
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'status_code': 'token_expired',
                'error': 'Token expired.'
            }, 401)
        # raise an error if auth0 information against is faulty
        except jwt.JWTClaimsError:
            raise AuthError({
                'status_code': 'invalid_claims',
                'error': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        # raise an error if the token cant be parsed
        except Exception:
            raise AuthError({
                'status_code': 'invalid_header',
                'error': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'status_code': 'invalid_header',
        'error': 'Unable to find the appropriate key.'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

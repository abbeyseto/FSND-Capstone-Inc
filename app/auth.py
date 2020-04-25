import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# AUTH0_DOMAIN='setoapps.auth0.com'
# ALGORITHMS=['RS256']
# API_AUDIENCE='capstone'
# CLIENT_ID='pudau6mZxjNgrN9PV1D0P7fjpXAob3wP'
# producer_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0Mzc2NTZiNjliYzBjMTJkNGIwY2IiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4MjI4OTYsImV4cCI6MTU4NzkwOTI5NiwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOkFjdG9ycyIsImRlbGV0ZTpNb3ZpZXMiLCJnZXQ6QWN0b3JzIiwiZ2V0Ok1vdmllcyIsInBhdGNoOkFjdG9ycyIsInBhdGNoOk1vdmllcyIsInBvc3Q6QWN0b3JzIiwicG9zdDpNb3ZpZXMiXX0.lK0eIfYVaip_R-EctPimb2xBY1hMDEgSQba0ABkGy0NiQG57LZYtJ5bGE9D_ikkXFulZA7f4n8Dd7kk8MyPjewojY8vlIcO7XuFxXdAusaJyZzCzoJRZ2Jop0DZlcFKn82f5pdc6yRp2hbe8ud3Od4KWqTp49eUzVE9W8Dt9PKjfVXJNJoZ7br25aaP9yZBXOYEBR1fvvNJ3A1SwtCk89I6HvwOxj1_MQ1x80qlL-F7cp0LnprXRMg7D8QEG7Dg9UKh0E5iNPlEIlDjVjJ99T1yGgbmEtqfBPW9eHiWppycQ4mKHQfXe3Phk4mTybXXcByB7NO5WG2caOt1c4zrTew"
# director_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0MzcyZjFjYzFhYzBjMTQ2NTIxNWEiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4MjI0NjUsImV4cCI6MTU4NzkwODg2NSwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOkFjdG9ycyIsImdldDpBY3RvcnMiLCJnZXQ6TW92aWVzIiwicGF0Y2g6QWN0b3JzIiwicGF0Y2g6TW92aWVzIiwicG9zdDpBY3RvcnMiXX0.JgwawfHTUgj1Kwg3UXqh-G3-xJ7KZZvhk44fSQH26IZ3hEUQY9yWT_Nv0GC3rdEnJLQfUUWOx9lbYbh6NjXIgoXz3elDRIl1e5-5EkbxZiV9v1bbwo-JLXjtVnpLCUW4UaMgrAJfEbyo4JvZn6H8nJIj09tFEPfBWA1Bmh_YBIPqaTGm5qCAOTdIcDO-O6Gys95O8zsysBYN4aNfWDo-II365VmP8tmjteTxTOktufE1bV1UMoH5zFFJGH35e6dgw4WeMxaTKz-hhGisYCNNIq0Pe0w2zConn8yBhQ_-wVgfkYVOeIVt2Ix9Ul48O-TH2x5gKEKfJdDcm5hAZWogyw"
# assistant_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0MzZmMTFjYzFhYzBjMTQ2NTIwZDkiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4MjIyNzUsImV4cCI6MTU4NzkwODY3NSwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OkFjdG9ycyIsImdldDpNb3ZpZXMiXX0.J0DE6nz1xQdD03G7Ton2iQzyv2zYx4op7axPVKPMfTykruUVcN2jO-iGm7dz7RD1SIHrtCLQGp1UCrsTlGjgKMhKJvTc92ESzn4iVZ7wz1BTn2Dmpx8Ps8FRGa5nPT2J2OzYXuTaZyUCPjXBnAaWkGmho2Oi5G_ruRyPz-LXRXRNZFOc6ZgNmqNPfFvpW_FRmZdhR7rvsQ4VvAUFrGjWORSm56wUL7DsCe38xB-_ZgUZPqUrKV7BXWLKPqTpIer-5sJleJXOE45fL5EoNAnmAFMJPt9aERjy4nwNAv3bmAwBmjwPBDRVZgl8MQdfT9NwFROGqf3qra2prtDJN7xbUQ"

AUTH0_DOMAIN=os.environ['AUTH0_DOMAIN']
ALGORITHMS=os.environ['ALGORITHMS']
API_AUDIENCE=os.environ['API_AUDIENCE']
CLIENT_ID=os.environ['CLIENT_ID']
producer_token=os.environ['producer_token']
director_token=os.environ['director_token']
assistant_token=os.environ['assistant_token']


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    header = request.headers['Authorization']
    header_parts = header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must ONLY be bearer token.'
        }, 401)

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims.\
                Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
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
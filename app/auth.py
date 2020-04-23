import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN='testfsnd.auth0.com'
ALGORITHMS=['RS256']
API_AUDIENCE='cap'
CLIENT_ID='29v4Ks9deL4ijNb06BvFHmZdk4WXeFtz'
producer_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0YzIyNGZmNzliYzBjNjUxZTIwMzMiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU0MzYsImV4cCI6MTU4NTA4MTgzNiwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpBY3RvcnMiLCJkZWxldGU6TW92aWVzIiwiZ2V0OkFjdG9ycyIsImdldDpNb3ZpZXMiLCJwYXRjaDpBY3RvcnMiLCJwYXRjaDpNb3ZpZXMiLCJwb3N0OkFjdG9ycyIsInBvc3Q6TW92aWVzIl19.me_VF-vIbYK3EBC_neJBKHaLJGBh4eQnKq7bCt62tIs1jZ2SeaiGVrKcjgMLQ0gT2eRS8tBfx9hkMPQkHudurn80G_whWtOcW4qjNs_DRdyVifqL0ANcBO0iYYgPuKdvxrwUm1sILpWY1rLJK-5FXdhZ42kiXbhsfM77KC7YTuEPmIXxK4Qfd5uHiBd-bmsiRV7HevQFSgv8lvWZ2jRcsQj9ceeC91puz1u580MBg3Olu-N0UCi7mnQyIIbxXjPcFtmFbdJA0myjRa6lUFyHnoZN9uFYjfI2aGc4hAvYuM5KpIHRE0Rw8RxH1kOCK18b1Xtth54kmbWcwNVcoXj3OA"
director_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0YzhiNjY3MzFkYzBjNjc1MGU4ZjkiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU3MzQsImV4cCI6MTU4NTA4MjEzNCwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpBY3RvcnMiLCJnZXQ6QWN0b3JzIiwiZ2V0Ok1vdmllcyIsInBhdGNoOkFjdG9ycyIsInBhdGNoOk1vdmllcyIsInBvc3Q6QWN0b3JzIl19.tmWxNIsZhR5NnHkM6t9xdKloFMutguDbkHpKLmLxFEt7oNRKdGb-Haol7OfnJzhfwdCUVucK4QxzoFutEXTBYABVMjfkMXhmwOlJPrbGp0fyyneI1_BpAK4VoihxD8iATZzBwoQOR7PBed9k4iM7phtmJYAA7OR2-72R_-0Fe29yUzQWdClPjoFIC_eVr_uLlHEqWDeBM6T8r-PTOPs8Hfs1_cA1yQXsCB08JipsKZ5pBB8AZEMIjkD1iymjdhIoLsXR2qDLuZU4iF6hveEJ1wdUZHg5JX5zU4jbiNGQcglup271P3QDIZ4RJzySukf4vA0h4ZpGkd1ypA83YBX9HA"
assistant_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0Yzk3N2ZmNzliYzBjNjUxZTM4YzAiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU5NTUsImV4cCI6MTU4NTA4MjM1NSwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpBY3RvcnMiLCJnZXQ6TW92aWVzIl19.oOIK6vRSLVCJksPH8_QSHgEGLBNqwi0grn7rmlvpCmKjBzhlIWuYYHttJQ5CNdeVXemw-fzphh8loVEpAPXykefvcFybo66R81Eu7Dc_SEBIidXkdVpYT3KVfZGEgYuEH8E-ZWokyAmrKtChCEOWD4ozNazDXAynvuhWHjFwKU4NIo-qdGqw-nm5kS0PRySfwxkQPA3yj55roQZcpxV8SF__IDY_HfnpJxyJiGUIyRHcZ8NOhJHHltGKLy8j16_79nLHshA2Csk1-9KJsabomfqK0ntlIjoNgaLeqsMR6ZoxoOxTNzyEQXpRSiHo2dE4rJ78VtpdNNiN1naJILeKBQ"



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
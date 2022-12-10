"""Authrider is a bodyguard for validating JWT Tokens"""
import os
from flask import Flask, jsonify, request
import jwt
from jwt import PyJWKClient

DEFAULT_ALGORITHMS = list(jwt.algorithms.get_default_algorithms().keys())[1:]

JWKS_URL = os.environ.get('JWKS_URL')
JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE')
JWT_ISSUER = os.environ.get('JWT_ISSUER')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_CLAIMS = os.environ.get('JWT_CLAIMS')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

if JWT_SECRET is None and JWKS_URL is None:
    raise Exception('JWT_SECRET|JWKS_URL is not set')
if JWT_ALGORITHM is None:
    raise Exception(
        f'JWT_ALGORITHM is not set, available algorithms: {", ".join(DEFAULT_ALGORITHMS)}'
    )
if JWT_ALGORITHM not in DEFAULT_ALGORITHMS:
    raise Exception(
        f'JWT_ALGORITHM is not valid, available algorithms: {", ".join(DEFAULT_ALGORITHMS)}'
    )

jwks_client = PyJWKClient(JWKS_URL)

def verify_token(token):
    """Verify JWT Token
    Args:
        token (str): JWT Token
    Returns:
        dict: Decoded JWT Token
    """
    secret = jwks_client.get_signing_key_from_jwt(token).key if JWKS_URL else JWT_SECRET
    return jwt.decode(
        token,
        secret,
        [JWT_ALGORITHM],
        audience=JWT_AUDIENCE,
        issuer=JWT_ISSUER
    )

app = Flask(__name__)

@app.route('/validate', methods=['GET'])
def index():
    """Validate JWT Token"""
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'Missing Authorization Header'}), 403
    jwt_token = request.headers['Authorization'].split(' ')[1]
    resp = None
    try:
        payload = verify_token(jwt_token)
        resp = jsonify({'message': 'Valid Token'}), 200
        if JWT_CLAIMS:
            for claim in JWT_CLAIMS.split(';'):
                header, value = claim.split(':')
                resp[0].headers[header] = payload[value]
    except jwt.ExpiredSignatureError:
        resp = jsonify({'message': 'Token Expired'}), 403
    except jwt.InvalidAudienceError:
        resp = jsonify({'message': 'Invalid Audience'}), 403
    except jwt.InvalidIssuerError:
        resp = jsonify({'message': 'Invalid Issuer'}), 403
    except jwt.InvalidTokenError:
        resp = jsonify({'message': 'Invalid Token'}), 403
    return resp
if __name__ == '__main__':
    app.run(port=3000, debug=True)

import os
from flask import Flask, jsonify, request
import jwt

JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE')
JWT_ISSUER = os.environ.get('JWT_ISSUER')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_CLAIMS = os.environ.get('JWT_CLAIMS')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

if JWT_SECRET is None:
    raise Exception('JWT_SECRET is not set')
if JWT_ALGORITHM is None:
    raise Exception('JWT_ALGORITHM is not set')

app = Flask(__name__)
@app.route('/validate', methods=['GET'])
def index():
    #return status code 403 if no authorization header is present and invalid jwt
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'Missing Authorization Header'}), 403
    jwt_token = request.headers['Authorization'].split(' ')[1]
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
        resp = jsonify({'message': 'Valid Token'}), 200
        if JWT_CLAIMS:
            for claim in JWT_CLAIMS.split(';'):
                header, value = claim.split(':')
                resp[0].headers[header] = payload[value]
        return resp
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token Expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid Token'}), 403
    except Exception as e:
        print(e)
        return jsonify({'message': 'Invalid Token'}), 403
if __name__ == '__main__':
    app.run(port=3000, debug=True)
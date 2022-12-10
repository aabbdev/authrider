# authrider
Authrider is the perfect bodyguard for validating JWT Tokens on your favorite reverse proxy like NGINX, Traefik.

#### Install with Docker
```bash
docker run -d --pull=always --name=authrider-1 --rm -p 3000:3000 -e JWT_ALGORITHM='HS256' -e JWT_SECRET='mysecret' ghcr.io/aabbdev/authrider:main
```

#### Environment variables
- JWT_ALGORITHM='HS256' (available algorithms: HS256, HS384, HS512, RS256, RS384, RS512, ES256, ES256K, ES384, ES521, ES512, PS256, PS384, PS512, EdDSA) *
- JWT_SECRET='YOUR SECRET or -----BEGIN PUBLIC KEY-----...' or JWKS_URL = "https://<YOUR_AUTH_PROVIDER>/.well-known/jwks.json" *
- JWT_CLAIMS='X-User:sub;X-Profile:profile' (Optional)
- JWT_ISSUER='https://authprovider.com' (Optional)
- JWT_AUDIENCE='http://localhost' (Optional)

#### Install with Docker compose

```yaml
version: '3.9'

services:
  authrider:
    image: ghcr.io/aabbdev/authrider:main
    environment:
      - JWT_SECRET=<your secret>
      - JWT_ALGORITHM=HS256
      - JWT_CLAIMS=X-User:sub
    ports:
      - "3000:3000"
```

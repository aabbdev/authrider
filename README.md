# authrider

Install with Docker
```bash
docker run -d --pull=always --name=authrider-1 --rm -p 3000:3000 -e JWT_ALGORITHM='HS256' -e JWT_SECRET='mysecret' ghcr.io/aabbdev/authrider:main
```

#### Environment variables
- JWT_ALGORITHM='HS256'
- JWT_SECRET='mysecret'
- (Optional) JWT_CLAIMS='X-User:sub;X-Profile:profile'
- (Optional) JWT_ISSUER='https://authprovider.com'
- (Optional) JWT_AUDIENCE='http://localhost'

Install with Docker compose

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

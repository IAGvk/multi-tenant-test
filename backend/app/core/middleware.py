from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM

class TenantMiddleware:
    def __init__(self, app):
        self.app = app
        self.security = HTTPBearer()

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization header missing")
        token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            scope["tenant_id"] = payload.get("tenant_id")
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
        await self.app(scope, receive, send)
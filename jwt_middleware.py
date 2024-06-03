from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from app.auth.jwt import SECRET_KEY, ALGORITHM
from app.services.user_service import UserService
from starlette.middleware.base import RequestResponseEndpoint

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in ["/user/login", "/user/register"]:
            return await call_next(request)

        if "authorization" not in request.headers:
            return JSONResponse(status_code=403, content={"detail": "Authorization header missing"})

        auth_header = request.headers["authorization"]
        token = auth_header.split(" ")[1] if " " in auth_header else None
        if not token:
            return JSONResponse(status_code=403, content={"detail": "Token missing"})

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=403, detail="Invalid token")
        except JWTError:
            return JSONResponse(status_code=403, content={"detail": "Invalid token"})

        user_service = UserService()
        user = await user_service.user_repository.get_user_by_email(email)
        if user is None:
            return JSONResponse(status_code=403, content={"detail": "User not found"})

        request.state.user = user
        return await call_next(request)

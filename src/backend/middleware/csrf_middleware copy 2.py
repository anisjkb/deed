# src/backend/middleware/csrf_middleware.py
import secrets
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import Response

class CsrfMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Generate a CSRF token if it's not already in the cookies
        csrf_token = request.cookies.get("csrf_access_token")
        if not csrf_token:
            csrf_token = secrets.token_hex(32)  # Generate a secure token

        response = await call_next(request)

        # Set the CSRF token cookie in the response with lowercase samesite="lax"
        response.set_cookie(
            "csrf_access_token", csrf_token, httponly=True, secure=True, samesite="lax"
        )

        return response

    def validate_csrf(self, request: Request):
        csrf_token_form = request.headers.get("X-CSRF-Token")
        csrf_token_cookie = request.cookies.get("csrf_access_token")

        if not csrf_token_form or csrf_token_form != csrf_token_cookie:
            raise HTTPException(status_code=403, detail="CSRF token mismatch")
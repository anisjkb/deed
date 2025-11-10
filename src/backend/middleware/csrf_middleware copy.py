# src/backend/middleware/csrf_middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from csrf_protect import CsrfProtect

class CsrfMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, csrf_protect: CsrfProtect):
        super().__init__(app)
        self.csrf_protect = csrf_protect

    async def dispatch(self, request: Request, call_next):
        # CSRF validation (for POST, PUT, DELETE, etc. methods)
        if request.method in ["POST", "PUT", "DELETE"]:
            self.csrf_protect.validate_csrf(request)
        
        response = await call_next(request)

        # Set CSRF cookie for all responses
        self.csrf_protect.set_csrf_cookie(response)

        return response
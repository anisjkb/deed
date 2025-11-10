# src/backend/middleware/security_headers.py
import secrets
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds modern security headers and a per-request CSP nonce.

    Usage:
        app.add_middleware(SecurityHeadersMiddleware, enable_hsts=settings.APP_ENV=='prod')
        In templates: <script nonce="{{ request.state.csp_nonce }}">...</script>
    """
    def __init__(self, app: ASGIApp, *, enable_hsts: bool = False) -> None:
        super().__init__(app)
        self.enable_hsts = enable_hsts

    async def dispatch(self, request: Request, call_next):
        # Generate a fresh CSP nonce per request
        nonce = secrets.token_urlsafe(16)
        request.state.csp_nonce = nonce

        response: Response = await call_next(request)

        # Core
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

        # Content Security Policy — allow only self, use nonce for inline scripts
        csp = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            f"script-src 'self' 'nonce-{nonce}'; "
            "style-src 'self' 'unsafe-inline'; "  # consider nonces for inline styles as follow-up
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers['Content-Security-Policy'] = csp

        # HSTS (HTTPS only)
        if self.enable_hsts and request.url.scheme == 'https':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        # Remove server banners if present
        if 'server' in response.headers:
            del response.headers['server']
        if 'x-powered-by' in response.headers:
            del response.headers['x-powered-by']

        return response
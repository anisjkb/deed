import os
from datetime import datetime, timedelta
import pytz
from typing import Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.utility.csrf import add_csrf, set_csrf_cookie  # Import CSRF functions

# Get the timezone from the .env file (e.g., "Asia/Dhaka")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
dhaka_tz = pytz.timezone(TIMEZONE)


def add_csrf_token(request: Request, context: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure CSRF token is added to the context."""
    # Retrieve or generate CSRF token from the session
    token = request.session.get("csrf_token", "GENERATED_TOKEN_12345")
    request.session["csrf_token"] = token  # Ensure it's stored in session
    context["csrf_token"] = token
    return context


def set_csrf_cookie(response: Response, token: str):
    """Sets the CSRF cookie in the response."""
    response.set_cookie(
        key="fastapi_csrf",
        value=token,
        httponly=True,
        secure=True,  # Use True in production (HTTPS)
        samesite="lax"
    )


class CSRFMiddleware(BaseHTTPMiddleware):
    """Middleware to set CSRF token in response headers and cookies."""

    async def dispatch(self, request: Request, call_next):
        """Generate CSRF token and set cookies/headers."""
        
        # 1. Generate/retrieve CSRF token and add it to context
        token_context = add_csrf_token(request, {"request": request})
        csrf_token: str = token_context.get("csrf_token", "")

        # 2. Process the request and get the response
        response = await call_next(request)

        # 3. Set the CSRF cookie/headers on the response
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type or "application/json" in content_type:
            set_csrf_cookie(response, csrf_token)
            response.headers["X-CSRF-Token"] = csrf_token

            # Optional: Set CSRF expiration info in the response headers
            current_time_dhaka = datetime.now(dhaka_tz)
            expiration_time_dhaka = current_time_dhaka + timedelta(hours=8)
            response.headers["X-CSRF-Expires"] = expiration_time_dhaka.strftime("%Y-%m-%dT%H:%M:%S%z")

        return response
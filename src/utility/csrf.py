# src/utility/csrf.py
import secrets, hmac
from fastapi import Request, HTTPException, Header, status
from starlette.responses import Response

# CSRF Configuration
CSRF_COOKIE_NAME = "csrftoken"
CSRF_FORM_FIELD = "csrf_token"
CSRF_HEADER_NAME = "X-CSRFToken"
CSRF_MAX_AGE = 60 * 60 * 8  # 8 hours

def _get_or_create_csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token

def set_csrf_cookie(response: Response, token: str):
    # Don't set HttpOnly so that frontend JS can read it for AJAX headers.
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=token,
        max_age=CSRF_MAX_AGE,
        path="/",
        secure=False,         # set True in production (HTTPS)
        httponly=False,       # False so JS can read it for AJAX
        samesite="lax" #Lax is a good balance between security and usability
    )

def add_csrf(request: Request, context: dict | None = None) -> dict:
    """Ensure CSRF token is added to the context."""
    token = _get_or_create_csrf_token(request)
    
    # If context is None or not a dictionary, initialize it as an empty dictionary.
    if context is None:
        context = {}

    if not isinstance(context, dict):
        raise ValueError("Expected context to be a dictionary.")

    context["csrf_token"] = token  # Add CSRF token to the context
    
    return context

async def csrf_protect(
    request: Request,
    csrf_from_header: str | None = Header(default=None, alias=CSRF_HEADER_NAME)
):
    # Accept token from either header (AJAX) or form (HTML)
    form_token = None
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded") or \
           request.headers.get("content-type", "").startswith("multipart/form-data"):
            form = await request.form()
            form_token = form.get(CSRF_FORM_FIELD)

        cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
        session_token = request.session.get("csrf_token")

        supplied = csrf_from_header or form_token
        if not supplied or not cookie_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing.")

        if not isinstance(supplied, str) or not isinstance(cookie_token, str) or not hmac.compare_digest(supplied, cookie_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token mismatch.")

        if not session_token or not hmac.compare_digest(supplied, session_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF session check failed.")
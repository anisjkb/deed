# src/backend/core/middleware.py
from fastapi import Request, Response, HTTPException
from src.core.config import get_settings
from src.utility.csrf import setup_secure_csrf, csrf_protect

def setup_custom_middleware(app):
    """Setup custom middleware (SessionMiddleware is already installed)"""
    settings = get_settings()
    
    # CSRF Protection Middleware
    @app.middleware("http")
    async def csrf_protection_middleware(request: Request, call_next):
        """Safe CSRF protection with session check"""
        
        # Log session ID and session data for debugging
        print(f"Session ID: {request.cookies.get('deed_session')}")  # Log session ID
        if "session" not in request.scope:
            print("⚠️ Session not available in request scope")
        else:
            print(f"Session Data: {dict(request.session.items())}")  # Log session data
        
        # Skip CSRF for safe methods and static files
        if should_skip_csrf(request):
            response = await call_next(request)
            return setup_secure_csrf(request, response)
        
        # For state-changing methods (POST, PUT, PATCH, DELETE), validate CSRF (with session access)
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            try:
                # Safe CSRF validation
                await csrf_protect(request)
            except Exception as e:
                if settings.DEBUG:
                    print(f"🔒 CSRF validation failed: {e}")
                raise e
        
        # Process the request and setup CSRF for the response
        response = await call_next(request)
        return setup_secure_csrf(request, response)
    
    # Additional middleware for awards context (you already have this part)
    @app.middleware("http")
    async def awards_context_middleware(request: Request, call_next):
        """Add awards context to request state"""
        request.state.awards = get_default_awards()
        response = await call_next(request)
        return response

async def safe_csrf_validate(request: Request):
    """Safe CSRF validation that checks for session availability"""
    # Check if session middleware is properly installed
    if "session" not in request.scope:
        raise HTTPException(
            status_code=500, 
            detail="Session middleware not available. Please contact administrator."
        )
    
    # Now safely validate CSRF token (calls csrf_protect)
    await csrf_protect(request)

def should_skip_csrf(request: Request) -> bool:
    """Determine if CSRF protection should be skipped"""
    # Skip safe methods
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return True
    
    # Skip API endpoints that use other auth methods (adjust for your app)
    if request.url.path.startswith(("/api/auth/", "/health", "/docs")):
        return True
    
    # Skip static files (e.g., images, CSS, JS)
    if request.url.path.startswith("/static/"):
        return True
    
    return False

def get_default_awards():
    """Default awards data (your context handling code)"""
    return {"awards": []}
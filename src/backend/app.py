# src/backend/app.py
import os
from datetime import datetime, timedelta
import pytz
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text

from src.backend.config import get_settings
from src.backend.database import engine
from src.backend.middleware.awards_context import AwardsContextMiddleware
from src.backend.routers import (
    get_routers,
    post_routers,
    projects,
    landowner,
    associate_business,
)
from src.utility.csrf import add_csrf, set_csrf_cookie
from dotenv import load_dotenv

# ───────────────────────────────────────────────
# Load environment + timezone
# ───────────────────────────────────────────────
load_dotenv()
TIMEZONE = os.getenv("TIMEZONE", "UTC")
dhaka_tz = pytz.timezone(TIMEZONE)
settings = get_settings()

# ───────────────────────────────────────────────
# Cache-friendly static class
# ───────────────────────────────────────────────
class ImmutableStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        resp = await super().get_response(path, scope)
        if 200 <= resp.status_code < 300:
            resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            resp.headers["Cache-Control"] = "no-store"
        return resp


# ───────────────────────────────────────────────
# FastAPI app setup
# ───────────────────────────────────────────────
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# ───────────────────────────────────────────────
# DB connection check (ping) on startup
# ───────────────────────────────────────────────
@app.on_event("startup")
async def startup_probe():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"[BOOT] Starting {settings.APP_NAME}")
    print(f"[BOOT] STATIC_VERSION = {settings.STATIC_VERSION}")
    print(f"[BOOT] DATABASE_URL (redacted host) = {settings.DATABASE_URL.split('@')[-1]}")

    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("[BOOT] ✅ Database connection OK")
    except Exception as ex:
        print("[BOOT] ❌ Database connection FAILED:")
        print("       ", ex)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


# ───────────────────────────────────────────────
# Session middleware (CSRF support)
# ───────────────────────────────────────────────
app.add_middleware(SessionMiddleware, secret_key="change-me-very-long-random")

# ───────────────────────────────────────────────
# CSRF middleware injection
# ───────────────────────────────────────────────
@app.middleware("http")
async def add_csrf_token(request: Request, call_next):
    response = await call_next(request)
    content_type = response.headers.get("Content-Type", "")

    if content_type == "":
        print("Content-Type header not found")
    elif "text/html" in content_type:
        print("This is an HTML response")
        context = add_csrf(request, {"request": request})

        current_time_dhaka = datetime.now(dhaka_tz)
        expiration_time_dhaka = current_time_dhaka + timedelta(hours=8)
        context["csrf_token_expiration"] = expiration_time_dhaka.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        set_csrf_cookie(response, context["csrf_token"])
        response.headers["X-CSRF-Token"] = context["csrf_token"]

        print("Injecting CSRF token:", context["csrf_token"])
    else:
        print("This is not an HTML response")

    return response


# ───────────────────────────────────────────────
# Templates setup
# ───────────────────────────────────────────────
templates = Jinja2Templates(directory="src/backend/templates")
templates.env.globals["assetv"] = settings.STATIC_VERSION
app.state.templates = templates

# ───────────────────────────────────────────────
# Static + middleware + routers
# ───────────────────────────────────────────────
app.mount("/static", ImmutableStaticFiles(directory="src/backend/static"), name="static")
app.add_middleware(AwardsContextMiddleware)

app.include_router(get_routers.router)
app.include_router(post_routers.router)
app.include_router(projects.router)
app.include_router(landowner.router)
app.include_router(associate_business.router)
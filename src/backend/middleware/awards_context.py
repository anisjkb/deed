# src/backend/middleware/awards_context.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy import select
from src.backend.database import get_db as get_session
from src.backend.models import Award


class AwardsContextMiddleware(BaseHTTPMiddleware):
    """
    Fetches awards from DB once per request and stores them on request.state.awards.
    Routes can then pass this into templates, or you can read it directly in templates
    via {{ request.state.awards }} if you expose 'request' to Jinja (we already do).
    """

    async def dispatch(self, request: Request, call_next):
        awards = []
        # Acquire a DB session using your existing generator
        try:
            async for session in get_session():
                result = await session.execute(select(Award))
                awards = result.scalars().all()
                break
        except Exception:
            # Fail-safe: don't block the page if DB temporarily fails
            awards = []

        # Stash on request.state
        request.state.awards = awards

        response = await call_next(request)
        return response
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(include_in_schema=False)

@router.get("/landowner", response_class=HTMLResponse)
async def landowner(request: Request):
    return request.app.state.templates.TemplateResponse(
        "landowner.html",
        {
            "request": request,
            "page_title": "Landowner — deed",
            "page_desc": "Partner with us for value & quality.",
            "awards": request.state.awards,
        },
    )
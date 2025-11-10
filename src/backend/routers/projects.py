# src/backend/routers/projects.py
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend.database import get_db as get_session
from src.backend.models import Project, ProjectType

router = APIRouter(tags=["projects"])

@router.get("/projects", response_class=HTMLResponse)
async def projects_index(
    request: Request,
    session: AsyncSession = Depends(get_session),
    category: str | None = None,
    type: str | None = None,
    location: str | None = None,
):
    q = select(Project)
    if category in {"ongoing", "upcoming", "completed"}:
        # status is a VARCHAR column; compare to string
        q = q.where(Project.status == category)
    if type in {"residential", "commercial"}:
        # ptype is an enum; bind via ProjectType
        q = q.where(Project.ptype == ProjectType(type))
    if location:
        q = q.where(Project.location.ilike(f"%{location}%"))

    projects = (await session.execute(q.order_by(Project.title))).scalars().all()

    return request.app.state.templates.TemplateResponse(
        "projects/index.html",
        {
            "request": request,
            "page_title": "Projects — deed",
            "page_desc": "All, Ongoing, Upcoming, Completed & filters for type and location.",
            "projects": projects,
            "category": category or "",
            "ptype": type or "",      # for the filter select
            "location": location or "",
            "awards": request.state.awards,
        },
    )

@router.get("/projects/{slug}", response_class=HTMLResponse)
async def project_detail(
    slug: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    project = (
        await session.execute(select(Project).where(Project.slug == slug))
    ).scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return request.app.state.templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "page_title": f"{project.title} — deed",
            "page_desc": project.short_desc or "",
            "project": project,
            "awards": request.state.awards,
        },
    )
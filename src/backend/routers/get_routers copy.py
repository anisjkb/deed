from fastapi import APIRouter, Depends, Request,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from pathlib import Path
import logging

from sqlalchemy import cast, String  # add at top with other imports
from src.backend.database import get_db as get_session
from src.backend.models import (
    Banner, Project, Testimonial, AssociateBusiness,
    EmpInfo, DesigInfo, OrgInfo
)
from src.utility.csrf import add_csrf, set_csrf_cookie

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Helper: Safe Template Rendering with CSRF
# ──────────────────────────────────────────────────────────────
def render_template(
    request: Request,
    template_name: str,
    page_title: str,
    page_desc: str,
    extra_ctx: dict | None = None
):
    awards = getattr(request.state, "awards", None)
    ctx = {
        "request": request,
        "page_title": page_title,
        "page_desc": page_desc,
        "awards": awards,
    }
    if extra_ctx:
        ctx.update(extra_ctx)

    ctx = add_csrf(request, ctx)
    resp = templates.TemplateResponse(template_name, ctx)
    set_csrf_cookie(resp, ctx["csrf_token"])
    resp.headers["X-CSRF-Token"] = ctx["csrf_token"]
    return resp

# ──────────────────────────────────────────────────────────────
# HOME PAGE (now also uses render_template for consistency)
# ──────────────────────────────────────────────────────────────
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    banners = featured_projects = testimonials = associated_business = []
    try:
        banners = (
            await session.execute(
                select(Banner).where(Banner.is_active == True).order_by(Banner.sort_order)
            )
        ).scalars().all()
    except SQLAlchemyError as e:
        log.warning("Home: banners query failed: %s", e)

    try:
        featured_projects = (
            await session.execute(select(Project).order_by(Project.title))
        ).scalars().all()
    except SQLAlchemyError as e:
        log.warning("Home: projects query failed: %s", e)

    try:
        testimonials = (
            await session.execute(select(Testimonial).order_by(Testimonial.sort_order))
        ).scalars().all()
    except SQLAlchemyError as e:
        log.warning("Home: testimonials query failed: %s", e)

    try:
        associated_business = (
            await session.execute(select(AssociateBusiness).order_by(AssociateBusiness.bus_name))
        ).scalars().all()
    except SQLAlchemyError as e:
        log.warning("Home: associate_business query failed: %s", e)

    return render_template(
        request,
        "index.html",
        "deed — Modern Real Estate in Dhaka",
        "Premium residences across Dhaka. Explore ongoing, upcoming & completed projects.",
        {
            "banners": banners,
            "featured_projects": featured_projects,
            "testimonials": testimonials,
            "associated_business": associated_business,
        }
    )

# ──────────────────────────────────────────────────────────────
# STATIC PAGES
# ──────────────────────────────────────────────────────────────
@router.get("/about-us", response_class=HTMLResponse)
async def about_us(request: Request):
    return render_template(
        request, "about.html", "About Us — deed", "Purpose, vision, values, timeline & leadership."
    )

# ──────────────────────────────────────────────────────────────
# DYNAMIC TEAM PAGE (robust enum filtering via TEXT cast)
# ──────────────────────────────────────────────────────────────
@router.get("/about-us/team", response_class=HTMLResponse)
async def about_team(request: Request, session: AsyncSession = Depends(get_session)):
    team_members = []
    try:
        q = (
            select(EmpInfo, DesigInfo.desig_name.label("desig_name"))
            .join(DesigInfo, EmpInfo.desig_id == DesigInfo.desig_id, isouter=True)
            # Cast enum column to TEXT so we compare with exact stored labels:
            .where(
                cast(EmpInfo.emp_type, String).in_([
                    "Management",
                    "Board Member",
                ])
            )
            .order_by(EmpInfo.sort_order.nulls_last(), EmpInfo.emp_name)
        )
        rows = (await session.execute(q)).all()
        team_members = [(row[0], row[1]) for row in rows]
    except SQLAlchemyError as e:
        log.warning("Team: query failed: %s", e)

    return render_template(
        request,
        "about_team.html",
        "Management Team — deed",
        "Leadership that delivers quality & trust.",
        {"team_members": team_members}
    )

# ──────────────────────────────────────────────────────────────
# TEAM MEMBER DETAIL
# ──────────────────────────────────────────────────────────────
@router.get("/about-us/team/{emp_id}", response_class=HTMLResponse)
async def team_member_detail(emp_id: str, request: Request, session: AsyncSession = Depends(get_session)):
    try:
        row = await session.execute(
            select(EmpInfo, DesigInfo.desig_name)
            .join(DesigInfo, EmpInfo.desig_id == DesigInfo.desig_id, isouter=True)
            .where(EmpInfo.emp_id == emp_id)
        )
        rec = row.first()
    except SQLAlchemyError as e:
        log.warning("Team detail: query failed: %s", e)
        rec = None

    if not rec:
        raise HTTPException(status_code=404, detail="Team member not found")

    emp, desig_name = rec
    page_title = f"{emp.emp_name} — deed"
    page_desc = desig_name or "Team member"

    return render_template(
        request,
        "about_team_detail.html",
        page_title,
        page_desc,
        {"emp": emp, "desig_name": desig_name}
    )

# ──────────────────────────────────────────────────────────────
# OTHER STATIC ROUTES
# ──────────────────────────────────────────────────────────────
@router.get("/about-us/timeline", response_class=HTMLResponse)
async def timeline(request: Request):
    return render_template(
        request, "about_timeline.html", "Timeline — deed", "Milestones and handovers across years."
    )

@router.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request):
    return render_template(
        request, "gallery.html", "Gallery — deed", "Photos, videos & newsletters."
    )

@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    return render_template(
        request, "blog.html", "Blog — deed", "Stories, updates & guides."
    )

@router.get("/career", response_class=HTMLResponse)
async def career(request: Request):
    return render_template(request, "career.html", "Career — deed", "Build with us.")

@router.get("/royal-club", response_class=HTMLResponse)
async def royal_club(request: Request):
    return render_template(
        request, "royal_club.html", "Royal Club — deed", "Benefits for valued residents & partners."
    )

@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy(request: Request):
    return render_template(
        request, "privacy.html", "Privacy Policy — deed", "Your data & privacy at deed."
    )

@router.get("/contact-us", response_class=HTMLResponse)
async def contact(request: Request, session: AsyncSession = Depends(get_session)):
    org = (
        await session.execute(
            select(OrgInfo).where(OrgInfo.status == "active").order_by(OrgInfo.org_id)
        )
    ).scalars().first()

    org_name = org.org_name if org else "Deed"
    org_address = org.org_address if org else "Dhaka-1000, Bangladesh"
    org_email = "contact@example.com"
    hotline = "0000-0000000"

    return render_template(
        request,
        "contact.html",
        "Contact — deed",
        "Reach us for site visits, bookings or partnerships.",
        {
            "org_name": org_name,
            "org_address": org_address,
            "org_email": org_email,
            "hotline": hotline,
        }
    )

@router.get("/feedback", response_class=HTMLResponse)
async def feedback(request: Request):
    return render_template(
        request, "feedback.html", "Share your feedback — deed", "Tell us how we can improve."
    )

@router.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return render_template(request, "thank_you.html", "Thank You — deed", "")

@router.get("/meetings", response_class=HTMLResponse)
async def meeting(request: Request):
    return render_template(
        request, "partials/_schedule_meeting.html", "Schedule A Meeting", "Book an appointment with us!"
    )

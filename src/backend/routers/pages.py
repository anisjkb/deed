# src/backend/routers/pages.py
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend.database import get_session
from src.backend.models import Banner, Project, Testimonial,AssociateBusiness

router = APIRouter(include_in_schema=False)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    banners = (
        await session.execute(
            select(Banner).where(Banner.is_active == True).order_by(Banner.sort_order)
        )
    ).scalars().all()

    featured_projects = (
        await session.execute(select(Project).limit(9))
    ).scalars().all()

    testimonials = (
        await session.execute(select(Testimonial).order_by(Testimonial.sort_order))
    ).scalars().all()

    associatedbusiness = (
        await session.execute(select(AssociateBusiness).order_by(AssociateBusiness.bus_name))
    ).scalars().all()
    
    return request.app.state.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_title": "deed — Modern Real Estate in Dhaka",
            "page_desc": "Premium residences across Dhaka. Explore ongoing, upcoming & completed projects.",
            "banners": banners,
            "featured_projects": featured_projects,
            "testimonials": testimonials,
            # awards are already fetched by middleware:
            "awards": request.state.awards,
            "associatedbusiness": associatedbusiness,
        },
        status_code=status.HTTP_200_OK,
    )

@router.get("/about-us", response_class=HTMLResponse)
async def about(request: Request):
    return request.app.state.templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "page_title": "About Us — deed",
            "page_desc": "Purpose, vision, values, timeline & leadership.",
            "awards": request.state.awards,
        },
    )

@router.get("/about-us/team", response_class=HTMLResponse)
async def team(request: Request):
    return request.app.state.templates.TemplateResponse(
        "about_team.html",
        {
            "request": request,
            "page_title": "Management Team — deed",
            "page_desc": "Leadership that delivers quality & trust.",
            "awards": request.state.awards,
        },
    )

@router.get("/about-us/timeline", response_class=HTMLResponse)
async def timeline(request: Request):
    return request.app.state.templates.TemplateResponse(
        "about_timeline.html",
        {
            "request": request,
            "page_title": "Timeline — deed",
            "page_desc": "Milestones and handovers across years.",
            "awards": request.state.awards,
        },
    )

@router.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request):
    return request.app.state.templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "page_title": "Gallery — deed",
            "page_desc": "Photos, videos & newsletters.",
            "awards": request.state.awards,
        },
    )

@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    return request.app.state.templates.TemplateResponse(
        "blog.html",
        {
            "request": request,
            "page_title": "Blog — deed",
            "page_desc": "Stories, updates & guides.",
            "awards": request.state.awards,
        },
    )

@router.get("/career", response_class=HTMLResponse)
async def career(request: Request):
    return request.app.state.templates.TemplateResponse(
        "career.html",
        {
            "request": request,
            "page_title": "Career — deed",
            "page_desc": "Build with us.",
            "awards": request.state.awards,
        },
    )

@router.get("/royal-club", response_class=HTMLResponse)
async def royal_club(request: Request):
    return request.app.state.templates.TemplateResponse(
        "royal_club.html",
        {
            "request": request,
            "page_title": "Royal Club — deed",
            "page_desc": "Benefits for valued residents & partners.",
            "awards": request.state.awards,
        },
    )

@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy(request: Request):
    return request.app.state.templates.TemplateResponse(
        "privacy.html",
        {
            "request": request,
            "page_title": "Privacy Policy — deed",
            "page_desc": "Your data & privacy at deed.",
            "awards": request.state.awards,
        },
    )

@router.get("/contact-us", response_class=HTMLResponse)
async def contact(request: Request):
    return request.app.state.templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "page_title": "Contact Us — deed",
            "page_desc": "Hotline, email & address.",
            "awards": request.state.awards,
        },
    )

@router.get("/feedback", response_class=HTMLResponse)
async def feedback(request: Request):
    return request.app.state.templates.TemplateResponse(
        "feedback.html",
        {
            "request": request,
            "page_title": "Share your feedback — deed",
            "page_desc": "Tell us how we can improve.",
            "awards": request.state.awards,
        },
    )

@router.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return request.app.state.templates.TemplateResponse(
        "thank_you.html",
        {
            "request": request,
            "page_title": "Thank you — deed",
            "awards": request.state.awards,
        },
    )
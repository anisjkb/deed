# src/backend/routers/associate_business.py
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend.database import get_db as get_session
from src.backend.models import AssociateBusiness
import logging  # Import logging for debugging

router = APIRouter(tags=["associate-business"])

@router.get("/associate-business", response_class=HTMLResponse)
async def associate_bussiness_index(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # Create a query to fetch businesses with published == 'Yes'
    q = select(AssociateBusiness).where(AssociateBusiness.published == 'Yes')
    
    # Execute the query and fetch all the businesses
    allbusiness = (await session.execute(q.order_by(AssociateBusiness.bus_name))).scalars().all()

    # Log the number of businesses fetched
    logging.info(f"Found {len(allbusiness)} businesses")

    # Pass allbusiness to the template as context
    return request.app.state.templates.TemplateResponse(
        "associate-businesses/index.html",
        {
            "request": request,
            "page_title": "Associate Business",
            "allbusiness": allbusiness,  # <-- Passing allbusiness here
            "awards": request.state.awards,  # <-- from middleware
        },
    )

@router.get("/associate-businesses/{bus_id}", response_class=HTMLResponse)
async def associate_business_detail(    
    request: Request,
    bus_id: int,
    session: AsyncSession = Depends(get_session)
):
    # Create a query to fetch the business by bus_id and ensure it is published
    q = select(AssociateBusiness).where(AssociateBusiness.bus_id == bus_id, AssociateBusiness.published == 'Yes')
    
    # Execute the query and fetch the business
    associatedbus = (await session.execute(q)).scalars().first()

    # If no business is found, raise a 404 error
    if not associatedbus:
        raise HTTPException(status_code=404, detail="Business not found")

    # Log the business details for debugging
    logging.info(f"Fetched business: {associatedbus.bus_name}")

    # Pass associatedbus to the template as context
    return request.app.state.templates.TemplateResponse(
        "associate-businesses/detail.html",
        {
            "request": request,
            "page_title": associatedbus.bus_name,
            "page_desc": associatedbus.description or "",
            "associatedbus": associatedbus,  # <-- Passing associatedbus here
            "awards": request.state.awards,  # <-- from middleware
        },
    )
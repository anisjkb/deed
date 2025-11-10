from fastapi import (
    APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
)
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
    # rollback/commit safety
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from typing import Optional

from src.backend.database import get_db as get_session
from src.backend.models import MeetingRequest, Feedback, LandownerLead
from src.utility.csrf import csrf_protect

router = APIRouter(prefix="/api", tags=["forms"])

@router.post("/meetings", dependencies=[Depends(csrf_protect)])
async def create_meeting(
    request: Request,
    session: AsyncSession = Depends(get_session),
    name: str = Form(...),
    phone: str = Form(...),
    email: Optional[str] = Form(None),
    preferred_date: Optional[str] = Form(None),
    preferred_time_slot: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    source_page: Optional[str] = Form(None),
):
    try:
        pd = None
        if preferred_date:
            try:
                y, m, d = preferred_date.split("-")
                pd = date(int(y), int(m), int(d))
            except ValueError:
                pd = None

        obj = MeetingRequest(
            name=name.strip(),
            phone=phone.strip(),
            email=email or None,
            preferred_date=pd,
            preferred_time_slot=preferred_time_slot or None,
            message=message or None,
            source_page=source_page or request.url.path
        )
        session.add(obj)
        await session.commit()
        return RedirectResponse(url="/thank-you", status_code=303)

    except SQLAlchemyError as e:
        await session.rollback()  # ✅ important
        #raise HTTPException(status_code=500, detail="Database error during meeting form save.")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", dependencies=[Depends(csrf_protect)])
async def create_feedback(
    request: Request,
    session: AsyncSession = Depends(get_session),
    name: str = Form(...),
    phone: str = Form(...),
    email: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
):
    try:
        obj = Feedback(
            name=name.strip(),
            phone=phone.strip(),
            email=email or None,
            message=message or None
        )
        session.add(obj)
        await session.commit()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JSONResponse({"success": True, "message": "Feedback received"})
        return RedirectResponse(url="/thank-you", status_code=303)

    except SQLAlchemyError as e:
        await session.rollback()  # ✅ important
        #raise HTTPException(status_code=500, detail="Database error during meeting form save.")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-image", dependencies=[Depends(csrf_protect)])
async def upload_image(file: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG or PNG allowed.")
    return {"filename": file.filename}

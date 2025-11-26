# src/backend/models.py
from __future__ import annotations
from datetime import date
from typing import Optional
import enum

from sqlalchemy import (
    DateTime, ForeignKey, String, Text, Integer, Date, Enum, Boolean, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.database import Base

# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────
class ProjectStatus(str, enum.Enum):
    ongoing = "ongoing"
    completed = "completed"
    upcoming = "upcoming"

class ProjectType(str, enum.Enum):
    residential = "residential"
    commercial  = "commercial"

class EmpType(str, enum.Enum):
    contractual   = "Contractual"
    permanent     = "Permanent"
    management    = "Management"
    board_member  = "Board Member"

# ──────────────────────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────────────────────
class Banner(Base):
    __tablename__ = "banners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String(500))
    headline: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    subhead: Mapped[Optional[str]] = mapped_column(String(300), default=None)
    cta_text: Mapped[Optional[str]] = mapped_column(String(64), default=None)
    cta_url: Mapped[Optional[str]] = mapped_column(String(300), default=None)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True)
    title: Mapped[str] = mapped_column(String(200))

    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="projectstatus", native_enum=True, create_type=False),
        default=ProjectStatus.ongoing,
    )
    ptype: Mapped[ProjectType] = mapped_column(
        Enum(ProjectType, name="projecttype", native_enum=True, create_type=False),
        default=ProjectType.residential,
    )

    tagline: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    location: Mapped[Optional[str]] = mapped_column(String(160), default=None)
    short_desc: Mapped[Optional[str]] = mapped_column(String(300), default=None)
    size_range: Mapped[Optional[str]] = mapped_column(String(120), default=None)

    floors: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    handover_date: Mapped[Optional[date]] = mapped_column(Date, default=None)
    hero_image_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)

    highlights: Mapped[Optional[str]] = mapped_column(Text, default=None)

class Award(Base):
    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    issuer: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    year: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    description: Mapped[Optional[str]] = mapped_column(String(400), default=None)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)

class Testimonial(Base):
    __tablename__ = "testimonials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    project_title: Mapped[Optional[str]] = mapped_column(String(160), default=None)
    quote: Mapped[str] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    published: Mapped[str] = mapped_column(String(3), default='Yes')

class MeetingRequest(Base):
    __tablename__ = "meeting_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(160))
    preferred_date: Mapped[Optional[date]] = mapped_column(Date)
    preferred_time_slot: Mapped[Optional[str]] = mapped_column(String(64))
    message: Mapped[Optional[str]] = mapped_column(Text)
    source_page: Mapped[Optional[str]] = mapped_column(String(160))
    # Store as timestamptz; DB fills in current timestamp (UTC internally)
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[Optional[str]] = mapped_column(String(160), default=None)
    message: Mapped[Optional[str]] = mapped_column(Text, default=None)
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=func.now())

class LandownerLead(Base):
    __tablename__ = "landowner_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[Optional[str]] = mapped_column(String(160), default=None)
    land_location: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    land_size: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    message: Mapped[Optional[str]] = mapped_column(Text, default=None)
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AssociateBusiness(Base):
    __tablename__ = "associate_business"

    bus_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bus_name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[date]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

class OrgInfo(Base):
    __tablename__ = "org_info"

    org_id: Mapped[str] = mapped_column(String(4), primary_key=True)
    group_id: Mapped[Optional[str]] = mapped_column(String(2), default=None)
    org_name: Mapped[str] = mapped_column(String(100))
    org_address: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    org_logo: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    status: Mapped[str] = mapped_column(String(20), default="active")

class DesigInfo(Base):
    __tablename__ = "desig_info"

    desig_id: Mapped[str] = mapped_column(String(2), primary_key=True)
    desig_name: Mapped[str] = mapped_column(String(100))
    sort_order: Mapped[Optional[int]] = mapped_column(Integer, default=None)

    employees = relationship("EmpInfo", back_populates="designation")

class EmpInfo(Base):
    __tablename__ = "emp_info"

    emp_id: Mapped[str] = mapped_column(String(6), primary_key=True)
    emp_name: Mapped[str] = mapped_column(String(100), nullable=False)

    emp_type: Mapped[EmpType] = mapped_column(
        Enum(
            EmpType,
            name="emp_type",
            native_enum=True,
            create_type=False,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=EmpType.contractual,
    )

    gender: Mapped[Optional[str]] = mapped_column(String(10), default=None)
    dob: Mapped[Optional[date]] = mapped_column(Date, default=None)
    mobile: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    email: Mapped[Optional[str]] = mapped_column(String(80), default=None)
    join_date: Mapped[Optional[date]] = mapped_column(Date, default=None)

    desig_id: Mapped[Optional[str]] = mapped_column(
        String(2),
        ForeignKey("desig_info.desig_id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    photo_url: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    bio: Mapped[Optional[str]] = mapped_column(Text, default=None)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(300), default=None)
    sort_order: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    status: Mapped[str] = mapped_column(String(20), default="active")
    bio_details: Mapped[Optional[str]] = mapped_column(Text, default=None)

    designation = relationship("DesigInfo", back_populates="employees")
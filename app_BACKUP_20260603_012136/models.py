from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.enums import CaseStatus


class Client(Base):
    __tablename__ = "clients"

    id                   = Column(Integer, primary_key=True, index=True)
    full_name            = Column(String(200), nullable=False)
    email                = Column(String(200), unique=True, index=True)
    phone                = Column(String(20))
    address              = Column(Text)
    city                 = Column(String(100))
    state                = Column(String(100))
    pincode              = Column(String(10))
    is_active            = Column(Boolean, default=True)
    portal_access        = Column(Boolean, default=False)
    portal_password_hash = Column(String(256))
    notes                = Column(Text)
    created_at           = Column(DateTime(timezone=True), server_default=func.now())
    updated_at           = Column(DateTime(timezone=True), onupdate=func.now())

    cases     = relationship("Case",     back_populates="client")
    documents = relationship("Document", back_populates="client")


class Case(Base):
    __tablename__ = "cases"

    id                  = Column(Integer, primary_key=True, index=True)
    client_id           = Column(Integer, ForeignKey("clients.id"), nullable=False)
    case_number         = Column(String(100), unique=True, index=True)
    title               = Column(String(300), nullable=False)
    case_type           = Column(String(100))
    cnr_number          = Column(String(50), index=True)
    filing_number       = Column(String(100))
    filing_year         = Column(String(10))
    registration_number = Column(String(100))
    registration_year   = Column(String(10))
    petitioner          = Column(String(300))
    respondent          = Column(String(300))
    case_stage          = Column(String(100))
    court               = Column(String(200))
    judge               = Column(String(200))
    ecourts_case_no     = Column(String(100))
    state_name          = Column(String(100))
    district_name       = Column(String(100))
    establishment_name  = Column(String(200))
    establishment_code  = Column(String(50))
    court_designation   = Column(String(200))
    purpose_name        = Column(String(200))
    last_hearing        = Column(DateTime(timezone=True))
    decision_date       = Column(DateTime(timezone=True))
    remarks             = Column(Text)
    status              = Column(Enum(CaseStatus), default=CaseStatus.pending)
    description         = Column(Text)
    next_hearing        = Column(DateTime(timezone=True))
    filing_date         = Column(DateTime(timezone=True))
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())

    client    = relationship("Client",   back_populates="cases")
    documents = relationship("Document", back_populates="case")
    hearings  = relationship("Hearing",  back_populates="case", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id          = Column(Integer, primary_key=True, index=True)
    client_id   = Column(Integer, ForeignKey("clients.id"))
    case_id     = Column(Integer, ForeignKey("cases.id"), nullable=True)
    filename    = Column(String(300), nullable=False)
    s3_key      = Column(String(500), nullable=False)
    file_size   = Column(Integer)
    file_type   = Column(String(50))
    description = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="documents")
    case   = relationship("Case",   back_populates="documents")


class Hearing(Base):
    __tablename__ = "hearings"

    id                = Column(Integer, primary_key=True, index=True)
    case_id           = Column(Integer, ForeignKey("cases.id"), nullable=False)
    hearing_date      = Column(DateTime(timezone=True), nullable=False)
    court_no          = Column(String(100))
    bench             = Column(String(200))
    stage_of_case     = Column(String(100))
    purpose           = Column(Text)
    proceedings       = Column(Text)
    order_summary     = Column(Text)
    next_hearing_date = Column(DateTime(timezone=True))
    effective_hearing = Column(Boolean, default=False)
    status            = Column(String(50), default="pending")
    created_at        = Column(DateTime(timezone=True), server_default=func.now())
    updated_at        = Column(DateTime(timezone=True), onupdate=func.now())

    case = relationship("Case", back_populates="hearings")


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String(200), unique=True, index=True)
    full_name       = Column(String(200))
    hashed_password = Column(String(256), nullable=False)
    is_active       = Column(Boolean, default=True)
    is_admin        = Column(Boolean, default=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

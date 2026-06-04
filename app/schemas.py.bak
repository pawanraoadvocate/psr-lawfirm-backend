from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.enums import CaseStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    is_admin: bool = False


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ClientCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ClientOut(BaseModel):
    id: int
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    is_active: bool
    portal_access: bool
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CaseCreate(BaseModel):
    client_id: int

    title: str

    case_type: Optional[str] = None
    court: Optional[str] = None
    judge: Optional[str] = None

    cnr_number: Optional[str] = None

    filing_number: Optional[str] = None
    filing_year: Optional[str] = None

    registration_number: Optional[str] = None
    registration_year: Optional[str] = None

    petitioner: Optional[str] = None
    respondent: Optional[str] = None
    case_stage: Optional[str] = None

    ecourts_case_no: Optional[str] = None

    state_name: Optional[str] = None
    district_name: Optional[str] = None

    establishment_name: Optional[str] = None
    establishment_code: Optional[str] = None

    court_designation: Optional[str] = None

    purpose_name: Optional[str] = None

    last_hearing: Optional[datetime] = None
    decision_date: Optional[datetime] = None

    remarks: Optional[str] = None

    description: Optional[str] = None
    next_hearing: Optional[datetime] = None
    filing_date: Optional[datetime] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None

    case_type: Optional[str] = None
    court: Optional[str] = None
    judge: Optional[str] = None

    cnr_number: Optional[str] = None

    filing_number: Optional[str] = None
    filing_year: Optional[str] = None

    registration_number: Optional[str] = None
    registration_year: Optional[str] = None

    petitioner: Optional[str] = None
    respondent: Optional[str] = None
    case_stage: Optional[str] = None

    status: Optional[CaseStatus] = None

    description: Optional[str] = None
    next_hearing: Optional[datetime] = None
    filing_date: Optional[datetime] = None


class CaseOut(BaseModel):
    id: int

    client_id: int

    case_number: str

    title: str

    case_type: Optional[str]
    court: Optional[str]
    judge: Optional[str]

    cnr_number: Optional[str]

    filing_number: Optional[str]
    filing_year: Optional[str]

    registration_number: Optional[str]
    registration_year: Optional[str]

    petitioner: Optional[str]
    respondent: Optional[str]
    case_stage: Optional[str]

    status: CaseStatus

    ecourts_case_no: Optional[str]

    state_name: Optional[str]
    district_name: Optional[str]

    establishment_name: Optional[str]
    establishment_code: Optional[str]

    court_designation: Optional[str]

    purpose_name: Optional[str]

    last_hearing: Optional[datetime]
    decision_date: Optional[datetime]

    remarks: Optional[str]

    description: Optional[str]

    next_hearing: Optional[datetime]
    filing_date: Optional[datetime]

    created_at: datetime

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: int
    client_id: int
    case_id: Optional[int]
    filename: str
    file_size: Optional[int]
    file_type: Optional[str]
    description: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True


class HearingCreate(BaseModel):
    case_id: int
    hearing_date: datetime

    court_no: Optional[str] = None
    bench: Optional[str] = None

    stage_of_case: Optional[str] = None

    purpose: Optional[str] = None
    proceedings: Optional[str] = None

    order_summary: Optional[str] = None

    next_hearing_date: Optional[datetime] = None

    effective_hearing: bool = False

    status: str = "Scheduled"


class HearingUpdate(BaseModel):
    hearing_date: Optional[datetime] = None

    court_no: Optional[str] = None
    bench: Optional[str] = None

    stage_of_case: Optional[str] = None

    purpose: Optional[str] = None
    proceedings: Optional[str] = None

    order_summary: Optional[str] = None

    next_hearing_date: Optional[datetime] = None

    effective_hearing: Optional[bool] = None

    status: Optional[str] = None


class HearingOut(BaseModel):
    id: int

    case_id: int

    hearing_date: datetime

    court_no: Optional[str]
    bench: Optional[str]

    stage_of_case: Optional[str]

    purpose: Optional[str]
    proceedings: Optional[str]

    order_summary: Optional[str]

    next_hearing_date: Optional[datetime]

    effective_hearing: bool

    status: str

    created_at: datetime

    class Config:
        from_attributes = True

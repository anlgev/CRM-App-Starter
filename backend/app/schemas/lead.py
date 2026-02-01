from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    company_name: str = Field(..., max_length=255)
    contact_name: str = Field(..., max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    source: Optional[str] = None


class LeadUpdate(BaseModel):
    company_name: Optional[str] = Field(None, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    is_active: Optional[bool] = None


class LeadOut(BaseModel):
    id: int
    company_name: str
    contact_name: str
    email: str
    phone: Optional[str]
    source: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

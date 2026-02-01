from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

DealStatus = Literal["Contacted", "Meeting", "Proposal", "Won", "Lost"]


class DealCreate(BaseModel):
    lead_id: int
    company_name: str
    status: DealStatus
    estimated_value: Optional[float] = Field(None, ge=0)
    next_action: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class DealUpdate(BaseModel):
    lead_id: Optional[int] = None
    company_name: Optional[str] = None
    status: Optional[DealStatus] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    next_action: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None
    closed_at: Optional[datetime] = None


class DealOut(BaseModel):
    id: int
    company_name: str
    status: DealStatus
    estimated_value: Optional[float]
    next_action: Optional[str]
    follow_up_date: Optional[datetime]
    created_at: datetime
    closed_at: Optional[datetime]
    notes: Optional[str]

    class Config:
        from_attributes = True

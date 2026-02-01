from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

ActivityAction = Literal["Email", "Call", "Meeting", "LinkedIn"]
ActivityResult = Literal["Replied", "No response", "Waiting"]


class ActivityCreate(BaseModel):
    lead_id: int
    company_name: str
    action_type: ActivityAction
    result: ActivityResult
    interested_person: Optional[str] = None
    date: datetime


class ActivityUpdate(BaseModel):
    lead_id: Optional[int] = None
    company_name: Optional[str] = None
    action_type: Optional[ActivityAction] = None
    result: Optional[ActivityResult] = None
    interested_person: Optional[str] = None
    date: Optional[datetime] = None


class ActivityOut(BaseModel):
    id: int
    lead_id: int
    company_name: str
    action_type: str
    result: str
    interested_person: Optional[str]
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

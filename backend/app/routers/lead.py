from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import create_db_engine
from app.models.lead import Lead

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/")
def create_lead(
    company_name: str,
    contact_name: str,
    email: str,
    is_active: bool = True,
    title: str | None = None,
    source: str | None = None,
    phone: str | None = None,
    db: Session = Depends(create_db_engine)
):
    lead = Lead(
        company_name=company_name,
        contact_name=contact_name,
        email=email,
        is_active=is_active,
        title=title,
        source=source,
        phone=phone
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.get("/")
def list_leads(db: Session = Depends(create_db_engine)):
    return db.query(Lead).all()

@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(create_db_engine)):
    lead = db.query(Lead).get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
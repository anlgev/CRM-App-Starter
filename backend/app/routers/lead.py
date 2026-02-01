from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import create_db_engine
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate, LeadOut

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(create_db_engine)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/", response_model=list[LeadOut])
def list_leads(db: Session = Depends(create_db_engine)):
    return db.query(Lead).all()


@router.patch("/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(create_db_engine)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(lead, k, v)

    db.commit()
    db.refresh(lead)
    return lead
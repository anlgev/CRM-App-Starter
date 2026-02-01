from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import create_db_engine
from app.models.deal import Deal

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("/")
def create_deal(
    company_name: str,
    lead_id: int,
    # company_id: int,
    status: str,
    estimated_value: float | None = None,
    db: Session = Depends(create_db_engine)
):
    deal = Deal(
        company_name=company_name,
        lead_id=lead_id,
        # company_id=company_id,
        status=status,
        estimated_value=estimated_value
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal

@router.get("/")
def list_deals(db: Session = Depends(create_db_engine)):
    return db.query(Deal).all()

@router.get("/{deal_id}")
def get_deal(deal_id: int, db: Session = Depends(create_db_engine)):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.activity import Activity
from datetime import datetime

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.post("/")
def create_activity(
    company_id: int,
    action_type: str,
    result: str,
    deal_id: int | None = None,
    db: Session = Depends(get_db)
):
    activity = Activity(
        company_id=company_id,
        deal_id=deal_id,
        action_type=action_type,
        result=result,
        date=datetime.utcnow()
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

@router.get("/")
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

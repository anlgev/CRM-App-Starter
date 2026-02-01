from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import create_db_engine
from app.models.activity import Activity
from datetime import datetime

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.post("/")
def create_activity(
    lead_id: int,
    company_name: str,
    # company_id: int,
    action_type: str,
    result: str,
    db: Session = Depends(create_db_engine)
):
    activity = Activity(
        lead_id=lead_id,
        company_name=company_name,
        # company_id=company_id,
        action_type=action_type,
        result=result,
        date=datetime.utcnow()
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

@router.get("/")
def list_activities(db: Session = Depends(create_db_engine)):
    return db.query(Activity).all()

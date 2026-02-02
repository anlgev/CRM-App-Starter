from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.activity import Activity
from datetime import datetime
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.post("/", response_model=ActivityOut)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    activity = Activity(**payload.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

@router.get("/", response_model=list[ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()


@router.patch("/{activity_id}", response_model=ActivityOut)
def update_activity(activity_id: int, payload: ActivityUpdate, db: Session = Depends(get_db)):
    activity = db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(activity, k, v)

    db.commit()
    db.refresh(activity)
    return activity

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import create_db_engine
from app.models.company import Company

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/")
def create_company(name: str, industry: str | None = None, db: Session = Depends(create_db_engine)):
    company = Company(name=name, industry=industry)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.get("/")
def list_companies(db: Session = Depends(create_db_engine)):
    return db.query(Company).all()

@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(create_db_engine)):
    company = db.query(Company).get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(create_db_engine)):
    company = db.query(Company).get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"deleted": True}

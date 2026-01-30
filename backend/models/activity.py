from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)

    date = Column(DateTime(timezone=True), nullable=False)
    action_type = Column(String, nullable=False)
    interested_person = Column(String, nullable=True)
    result = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

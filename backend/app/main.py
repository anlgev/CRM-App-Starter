from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import company, deal, activity

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM App")

app.include_router(company.router)
app.include_router(deal.router)
app.include_router(activity.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


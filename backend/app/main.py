from fastapi import FastAPI
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM App")

@app.get("/health")
def health_check():
    return {"status": "ok"}


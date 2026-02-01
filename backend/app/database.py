import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

def create_db_engine():
    for i in range(10):
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print("✅ Database connection successful")
            return engine
        except OperationalError:
            print(f"⏳ Database not ready, retrying ({i+1}/10)...")
            time.sleep(2)
    raise Exception("❌ Could not connect to database")

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
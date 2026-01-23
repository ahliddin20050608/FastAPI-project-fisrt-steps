from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.schemas.settings import settings

DATABASE_URL = settings.DB_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
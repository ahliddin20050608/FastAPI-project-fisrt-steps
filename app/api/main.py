from fastapi import FastAPI
from contextlib import asynccontextmanager, contextmanager
from sqlalchemy import text
from app.api.v1 import user_router
from app.schemas import settings
from app.db import SessionLocal
from app.services import remove_pycaches_ad_pycs
from app.schemas import BASE_DIR
from app.services import get_logger

import logging

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        logger.INFO("Database connected")
    except Exception as e:
        print("Database connection error",e)
    remove_pycaches_ad_pycs(BASE_DIR)
    
    yield

app = FastAPI(title="My first project FastAPI", version="1.0.0", lifespan=lifespan)

app.include_router(user_router, prefix="/api/v1/users")

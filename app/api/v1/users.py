from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User


user_router = APIRouter()

@user_router.get("/check_user/{chat_id}")
async def check_user(chat_id:str, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.chat_id==chat_id).first()
    
    if user is not None:
        return User
    data = {
        "status":False,
        "message":"User not found."
    }
    
    return Response(content=data, status_code=status.HTTP_404_NOT_FOUND)

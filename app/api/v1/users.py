from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, OTP
from app.schemas.user import  UserSchema
from utils.code import generate_secure_6_digit_code
from datetime import  datetime, timedelta
user_router = APIRouter()

@user_router.get("/check_user/{chat_id}")
async def check_user(chat_id:str, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.chat_id==chat_id).first()
    
    if user is not None:
        return user
    data = {
        "status":False,
        "message":"User not found."
    }
    
    return JSONResponse(content=data, status_code=status.HTTP_404_NOT_FOUND)



@user_router.get("/register")
async def register_user(user:UserSchema, db:Session = Depends(get_db)):
    try:
        user_db = User(
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        chat_id = user.chat_id,
        phone_number = user.phone_number

        )
        db.add(user_db)
        db.commit()
        
        code = generate_secure_6_digit_code()
        while db.query(OTP).filter(OTP.code==code).first():
            code = generate_secure_6_digit_code()
        otp = OTP(
            user_id=user_db.id,
            code=code,
            expired_at=datetime.utcnow()+timedelta(minutes=2),
            is_active=True
        )
        db.add(otp)
        db.commit()
        data = {
            "status":True,
            "message":"User registrated succesfully",
            "code":code
        }
        return JSONResponse(content=data, status=status.HTTP_200_OK)
    except Exception as e:
        data = {
            "status":False,
            "message":f"Error-{e} "
        }
    
        return JSONResponse(content=data, status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


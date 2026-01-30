from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, OTP
from app.schemas.user import UserSchema, CodeSchema
from utils.code import generate_secure_6_digit_code
from datetime import datetime,timedelta
from sqlalchemy.exc import IntegrityError
from utils.auth import create_access_token

user_router = APIRouter()

@user_router.get("/check_user/{chat_id}")
async def check_user(chat_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.chat_id == chat_id).first()
    if user:
        return {"status": True, "message": "User found."}
    return JSONResponse(
        content={"status": False, "message": "User not found."},
        status_code=status.HTTP_404_NOT_FOUND
    )

@user_router.post("/register")
async def register_user(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.chat_id == user.chat_id).first()
    if existing_user:
        return JSONResponse(
            content={"status": False, "message": "User already exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        user_db = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            chat_id=user.chat_id,
            phone_number=user.phone_number
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        code = generate_secure_6_digit_code()
        while db.query(OTP).filter(OTP.code == code).first():
            code = generate_secure_6_digit_code()

        otp = OTP(
            user_id=user_db.id,
            code=code,
            expired_at=datetime.utcnow() + timedelta(minutes=2),
            is_active=True
        )
        db.add(otp)
        db.commit()

        return {
            "status": True,
            "message": "User registered successfully",
            "code": code
        }

    except IntegrityError:
        db.rollback()
        return JSONResponse(
            content={"status": False, "message": "User already exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"status": False, "message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
  
      )

def is_expired_code(otp:OTP):
    if otp.expired_at < datetime.utcnow():
        return otp
        
@user_router.get(path="/check_otp/{chat_id}")
async def check_otp(chat_id:str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.chat_id==chat_id).first()
    if user is not None:
        otp = db.query(OTP).filter(OTP.user_id==user.id).order_by(OTP.expired_at.desc()).first()
        if otp is not None and not is_expired_code(otp):
            data = {
                "status":"old",
                "message":"You have a verification code that is not expired.",
                "otp":otp
            }            
        
            return data 
        code = generate_secure_6_digit_code()
        while db.query(OTP).filter(OTP.code == code).first():
            code = generate_secure_6_digit_code()

        otp = OTP(
            user_id=user.id,
            code=code,
            expired_at=datetime.utcnow() + timedelta(minutes=2),
            is_active=True
        )
        db.add(otp)
        db.commit()
        db.refresh(otp)
        data = {
                "status":"new",
                "message":"New OTP code created.",
                "otp":otp
        }    
            
    else:
        return  HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
@user_router.post(path="/token")
async def verify_user(code:CodeSchema, db:Session=Depends(get_db)):
    code = code.code
    otp = db.query(OTP).filter(OTP.code==code).first()
    if otp is not None:
        if not is_expired_code(otp=otp):
            data = {"sub":otp.user.phone_number}
            token = create_access_token(data=data)  
            data = {
                "access_token":str(token),
                "access_type":"bearer"
            }
        else:
            data = {
                "status":False,
                "message":"Code has expired"
            }
        return data
    else:{
        "status":False,
        "message":"Invalid code"
     }
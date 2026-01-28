from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime
from typing import List
class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String(100))
    last_name:Mapped[str] = mapped_column(String(100))
    username:Mapped[str] = mapped_column(String(100), unique=True)
    phone_number:Mapped[str] = mapped_column(String(20), unique=True)
    is_active:Mapped[bool] = mapped_column(default=False)
    chat_id:Mapped[str] = mapped_column(String(20))
    otps:Mapped[List["OTP"]] = relationship(back_populates="users")
    
class OTP(Base):
    __tablename__ = "otps"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    code:Mapped[str] = mapped_column(String(6), unique=True)
    expired_at:Mapped[datetime] = mapped_column(DateTime)
    is_active:Mapped[bool] = mapped_column(default=False)
    
    user:Mapped["User"] = relationship(back_populates="otps")
    
    

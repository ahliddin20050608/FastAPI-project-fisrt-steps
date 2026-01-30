from app.schemas.settings import settings
from jose import jwt
from datetime import datetime, timedelta
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.DEFAULT_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
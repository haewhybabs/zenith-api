# src/auth/jwt.py
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from src.config import settings  # <--- Importing the loaded config

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Passing the expire minutes to timedelta
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Passing SECRET_KEY and ALGORITHM to the jwt library
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
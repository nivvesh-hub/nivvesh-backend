# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt,  JWTError
import os

# Ideally, load these settings from environment variables or a configuration file
SECRET_KEY = os.getenv("SECRET_KEY", "HLhZGKeaxKVQsYVk6uq5qh1spUOuHdJjUdoyA5viNyU")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict) -> str:
    """Create a JWT token with expiration and additional claims."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import settings
from database import get_db
import models
from schemas.user import TokenData

import bcrypt

# Use OAuth2PasswordBearer so FastAPI automatically maps Swagger UI logins
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# We removed passlib and use bcrypt directly to avoid passlib max password bug on python 3.13
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default fallback
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Base Dependency to extract the current user from DB
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        nim_npp: str = payload.get("sub")
        if nim_npp is None:
            raise credentials_exception
        token_data = TokenData(nim_npp=nim_npp)
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.nim_npp == token_data.nim_npp).first()
    if user is None:
        raise credentials_exception
    return user

# RBAC Middleware Wrapper
def require_role(allowed_roles: list[models.RoleEnum]):
    """Returns a dependency function checking if current user's role is permitted."""
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions for this action"
            )
        return current_user
    return role_checker

# Convenient Dependency Pointers
get_admin = require_role([models.RoleEnum.admin])
get_petugas = require_role([models.RoleEnum.petugas, models.RoleEnum.admin])
get_mahasiswa = require_role([models.RoleEnum.mahasiswa])

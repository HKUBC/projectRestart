from datetime import UTC, datetime, timedelta
from tokenize import Token
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.db.models.user_information.user_table import users
from app.db.db_setup import get_db
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordBearer
from jose import jwt, JWTError
from app.api.config import settings



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# Authentication Methods
def hash_password(password: str)->str:
    return bcrypt_context.hash(password)
def verify_password(plain_password: str, hashed_password: str)-> bool:
    return bcrypt_context.verify(plain_password, hashed_password)
def create_access_token(data: dict, expires_delta: timedelta | None = None)-> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(settings.access_token_expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm = settings.algorithm)
    return encoded_jwt
def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms = settings.algorithm,
            options = {"require": ["exp", "sub"]}

        )
    except JWTError:
         raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token")
    else: 
        return payload.get("sub")




from fastapi import Depends, status
from fastapi.exceptions import ValidationException, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt
from typing import Union, Any, Optional, Annotated
from datetime import datetime, timedelta
import pytz
from src.database import get_async_session
from .config import *
from .schemas import TokenAccessData, UserSchema
from .models import UserModel


oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_hashed_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def create_access_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = TokenAccessData(
        email=subject.email, first_name=subject.first_name, phone=subject.phone,
        last_name=subject.last_name, token_type='access', exp=expires_delta
    )
    encode_jwt = jwt.encode(token_data.model_dump(), JWT_SECRET_KEY, ALGORITHM)
    return encode_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow().replace(tzinfo=pytz.utc) + expires_delta
    else:
        expires_delta = datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {'token_type': 'refresh', 'exp': expires_delta, 'sub': str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encode_jwt




async def get_current_user(
        token: str = Depends(oauth), session: AsyncSession = Depends(get_async_session)
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenAccessData(**payload)
        print(token_data.exp, datetime.utcnow())
        if token_data.exp.replace(tzinfo=pytz.utc) < datetime.utcnow().replace(tzinfo=pytz.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Токен просроченный',
                headers={'WWW-Authenticate': 'Bearer'}
            )
    except (jwt.JWTError, ValidationException):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    stat = select(UserModel).where(UserModel.email == token_data.email)
    data = await session.execute(stat)
    user = data.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user


async def authenticate_user(user: Annotated[UserModel, Depends(get_current_user)]):
    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
    return UserSchema(**user_dict)




























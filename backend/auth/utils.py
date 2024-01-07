from typing import Union, Any, Optional, Annotated

from fastapi import Depends, status
from fastapi.exceptions import ValidationException, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

import pytz

from jose import jwt

from datetime import datetime, timedelta

from backend.database import get_async_session
from backend.utils import async_send_mail
from .config import *
from .schemas import TokenAccessData, UserSchema
from .models import UserModel


oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    """Transform a user's password to hash"""
    return password_context.hash(password)


def verify_hashed_password(password, hashed_password):
    """Verify a user's password from hash"""
    return password_context.verify(password, hashed_password)


def create_access_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create an access jwt token for a user"""

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
    """Create a refresh token for user"""
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {'token_type': 'refresh', 'exp': expires_delta, 'sub': str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encode_jwt


async def get_user_from_db(email: str, session: AsyncSession = Depends(get_async_session)):
    """Get a user from db by email"""

    stat = select(UserModel).where(UserModel.email == email)
    data = await session.execute(stat)
    user = data.scalars().first()

    return user


async def get_current_user(
        token: str = Depends(oauth), session: AsyncSession = Depends(get_async_session)
):
    """Get a current user with usage a jwt token"""

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenAccessData(**payload)

        if token_data.exp.replace(tzinfo=pytz.utc) < datetime.utcnow().replace(tzinfo=pytz.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token has been expired',
                headers={'WWW-Authenticate': 'Bearer'}
            )
    except (jwt.JWTError, ValidationException):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_from_db(token_data.email, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dont found the user",
        )

    return user


async def authenticate_user(user: Annotated[UserModel, Depends(get_current_user)]):
    """Authorize a user"""
    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}

    return UserSchema(**user_dict)


async def authenticate_staff(user: Annotated[UserModel, Depends(get_current_user)]):
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You dont have the permission'
        )
    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
    return UserSchema(**user_dict)


async def send_email_for_verify(email: str, first_name: str, last_name: str) -> None:
    expired = datetime.utcnow() + timedelta(minutes=50)
    to_encode = {
        'email': email, 'exp': expired, 'purpose': 'verification'
    }
    token = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    body = {'first_name': first_name, 'last_name': last_name, 'token': token}
    await async_send_mail('Подтверждение электронной почты', email, body, 'verify.html')

































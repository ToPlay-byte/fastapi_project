from fastapi import APIRouter, Depends, Form, status
from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from jose import jwt
from typing import Annotated
from src.database import get_async_session
from .config import JWT_SECRET_KEY, ALGORITHM
from .utils import *
from .schemas import UserCreateSchema, UserUpdateSchema
from .models import UserModel

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/create_user')
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    try:
        dict_user = user.model_dump()
        password = get_hashed_password(dict_user.pop('password'))
        stat = insert(UserModel).values(
            **dict_user, password=password, is_verified=False,
            is_superuser=False, is_staff=False
        )
        await session.execute(stat)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exist'
        )
    await send_email_for_verify(user.email, user.first_name, user.last_name)
    return {'status': 'The user has been created'}


@router.patch('/update_user')
async def update_user(
        changed_user: UserUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserSchema = Depends(authenticate_user)
):
    stat = update(UserModel).values(**changed_user.model_dump()).where(UserModel.email == current_user.email)
    await session.execute(stat)
    await session.commit()
    return {'status': 'The user\'s data has been updated'}


@router.post('/login')
async def login(
        email: Annotated[str, Form(pattern=r'^[A-Za-z.0-9_-]+@[A-Za-z0-9-]+\.[A-Za-z]+$')],
        password: Annotated[str, Form(min_length=8, max_length=16)],
        session: AsyncSession = Depends(get_async_session)
):
    user = await get_user_from_db(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неправильный пароль или почта')
    if not verify_hashed_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неправильный пароль или почта')
    return {
        'access_token': create_access_token(user),
        'refresh': create_refresh_token(user.email)
    }


@router.patch('/confirm_email/{token}')
async def confirm_email(token: str, session: AsyncSession = Depends(get_async_session)):
    token_data = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    expired = token_data.get('exp')
    if datetime.fromtimestamp(expired) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен просроченный',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    stat = update(UserModel).values(is_verified=True).where(UserModel.email == token_data.get('email'))
    await session.execute(stat)
    await session.commit()
    return {'status': 'The user has been verified'}

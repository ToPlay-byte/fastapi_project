from fastapi import APIRouter, Form

from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError

from pydantic import EmailStr

from .utils import *
from .schemas import UserCreateSchema, UserUpdateSchema
from .models import UserModel


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/create_user')
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    """Create a new user"""

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
    """Update a user by email"""

    stat = update(UserModel).values(**changed_user.model_dump()).where(UserModel.email == current_user.email)
    await session.execute(stat)
    await session.commit()

    return {'status': 'The user\'s data has been updated'}


@router.post('/login')
async def login(
        email: Annotated[EmailStr, Form()],
        password: Annotated[str, Form(min_length=8, max_length=16)],
        session: AsyncSession = Depends(get_async_session)
):
    """Authorize a user"""

    user = await get_user_from_db(email, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password or email')
    if not verify_hashed_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password or email')

    return {
        'access_token': create_access_token(user),
        'refresh': create_refresh_token(user.email)
    }


@router.patch('/confirm_email/{token}')
async def confirm_email(token: str, session: AsyncSession = Depends(get_async_session)):
    """Confirm a user's email"""

    token_data = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    expired = token_data.get('exp')

    if datetime.fromtimestamp(expired) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token has been expired```````',
        )

    if not token_data.get('verification') == 'verification':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This token doesnt use for verification email',
        )

    stat = update(UserModel).values(is_verified=True).where(UserModel.email == token_data.get('email'))
    await session.execute(stat)
    await session.commit()

    return {'status': 'The user has been verified'}


@router.post('/reset_password/')
async def reset_password(email: Annotated[EmailStr, Form()], session: AsyncSession = Depends(get_async_session)):
    """Send an email to a user to reset his password"""

    stat = select(UserModel).where(UserModel.email == email)
    result = await session.execute(stat)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user with email doesnt exist+',
        )

    expired = datetime.utcnow() + timedelta(minutes=10)
    to_encode = {'email': email, 'exp': expired, 'purpose': 'reset_password'}
    token = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    body = {'first_name': user.first_name, 'last_name': user.last_name, 'token': token}

    await async_send_mail('Сброс пароля', email, body, 'reset_password.html')

    return {'status': 'The letter has been send to your email'}


@router.post('/reset_password_confirm/{token}')
async def reset_password_confirm(
        token: str,
        password: Annotated[str, Form(min_length=8, max_length=16)],
        session: AsyncSession = Depends(get_async_session)
):
    """Reset a user's password"""

    token_data = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    expired = token_data.get('exp')

    if datetime.fromtimestamp(expired) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token has been expired',
        )

    if not token_data.get('purpose') == 'reset_password':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This token doesnt use for reset password',
        )

    stat = update(UserModel).values(password=password).where(UserModel.email == token_data.get('email'))
    await session.execute(stat)
    await session.commit()

    return {'status': 'The user\'s password has been changed'}











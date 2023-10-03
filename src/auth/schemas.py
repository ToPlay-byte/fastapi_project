from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: str = Field(pattern=r'^[A-Za-z.0-9_-]+@[A-Za-z0-9-]+\.[A-Za-z]+$')
    phone: str = Field(pattern=r'^\(380\)[0-9]{9}')


class UserCreateSchema(UserSchema):
    password: str = Field(max_length=16, min_length=8)


class UserUpdateSchema(BaseModel):
    __annotations__ = {key: Optional[value] for key, value, in UserSchema.__annotations__.items()}


class TokenAccessData(UserSchema):
    exp: datetime
    token_type: str

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    """This is a base schema of a user"""
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    phone: str = Field(pattern=r'^\(380\)[0-9]{9}')


class UserCreateSchema(UserSchema):
    """This schema is used to create a user """
    password: str = Field(max_length=16, min_length=8)


class UserUpdateSchema(BaseModel):
    """This schema is used to update a user """
    __annotations__ = {key: Optional[value] for key, value, in UserSchema.__annotations__.items()}


class TokenAccessData(UserSchema):
    """A base schema of an access token """
    exp: datetime
    token_type: str

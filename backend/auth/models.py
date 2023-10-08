from fastapi import Depends
from sqlalchemy import String, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_superuser: Mapped[bool] = mapped_column()
    is_verified: Mapped[bool] = mapped_column()
    is_staff: Mapped[bool] = mapped_column()
    password: Mapped[str] = mapped_column(String(150))




from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class UserModel(Base):
    """A general user's model"""
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




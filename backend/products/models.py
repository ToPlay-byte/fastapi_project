from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import Text, String, ForeignKey


Base = declarative_base()


class ProductModel(Base):
    """A general product's model"""
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(ForeignKey('categories.name'))
    price: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    banner: Mapped[str] = mapped_column(String(50), nullable=False)


class Category(Base):
    """A general category's model"""
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)


class ProductImage(Base):
    """A image's model for product"""
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    product: Mapped[id] = mapped_column(ForeignKey('products.id'), nullable=False)




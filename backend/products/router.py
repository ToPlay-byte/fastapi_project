from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

from backend.database import get_async_session
from backend import UserSchema, authenticate_user
from .schemas import ProductSchema, CategorySchema
from .models import ProductModel, Category


router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.post('/create_product')
async def create_product(product: ProductSchema, session: AsyncSession = Depends(get_async_session)):
    """Create a new product"""

    stat = insert(ProductModel).values(**product.model_dump())
    await session.execute(stat)
    await session.commit()

    return {'status': 'The product has been created'}


@router.get('/get_list_products')
async def get_list_products(
        session: AsyncSession = Depends(get_async_session),
        user: UserSchema = Depends(authenticate_user)
):
    """Get all products"""

    stat = select(ProductModel)
    result = await session.execute(stat)
    return result.scalars().all()


@router.get('/get_product')
async def get_product(product_name: str, session: AsyncSession = Depends(get_async_session)):
    """Get a product by name"""

    stat = select(ProductModel).where(ProductModel.name == product_name)
    result = await session.execute(stat)
    return result.scalars().all()[0]


@router.put('/change_product/{product_name}')
async def change_product(
        product_name: str,
        product: ProductSchema,
        session: AsyncSession = Depends(get_async_session)
):
    """Change a product by name"""

    stat = update(ProductModel).where(ProductModel.name == product_name).values(**product.model_dump())
    result = await session.execute(stat)

    if result.rowcount:
        await session.commit()
        return {'success': 'The product has been updated'}
    else:
        return {'error': 'Doesn`t found the product'}


@router.get('/get_categories_list')
async def get_categories_list(session: AsyncSession = Depends(get_async_session)):
    """Get all categories"""

    stat = select(Category)
    result = await session.execute(stat)

    return result.scalars().all()


@router.post('/create_category')
async def create_category(category: CategorySchema, session: AsyncSession = Depends(get_async_session)):
    """Create a new category"""

    stat = insert(Category).values(**category.model_dump())
    await session.execute(stat)
    await session.commit()

    return {'status': 'The category has been created successfully'}


@router.delete('/delete_category')
async def delete_category(category_name: str,  session: AsyncSession = Depends(get_async_session)):
    """Delete  a category"""

    stat = delete(Category).where(Category.name == category_name)
    await session.execute(stat)
    await session.commit()

    return {'status': 'The category has been deleted'}

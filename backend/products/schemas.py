from pydantic import BaseModel
from typing import Optional


class CategorySchema(BaseModel):
    """A base schema of a category"""
    name: str


class ProductSchema(BaseModel):
    """A base schema of a product"""
    name: str
    category: str
    price: int
    description: str
    quantity: int
    banner: str


class UpdateProductSchema(ProductSchema):
    """This schema is used for update a product"""
    __annotations__ = {k: Optional[v] for k, v in ProductSchema.__annotations__.items()}


class ProductImage(BaseModel):
    """A base schema of an image for product"""
    image: str
    product: str

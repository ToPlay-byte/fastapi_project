from pydantic import BaseModel, Field
from typing import Optional


class CategorySchema(BaseModel):
    name: str


class ProductSchema(BaseModel):
    name: str
    category: str
    price: int
    description: str
    quantity: int
    banner: str


class UpdateProductSchema(ProductSchema):
    __annotations__ = {k: Optional[v] for k, v in ProductSchema.__annotations__.items()}


class Images(BaseModel):
    image: str
    product: str

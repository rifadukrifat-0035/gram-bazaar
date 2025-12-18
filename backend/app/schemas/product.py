# backend/app/schemas/product.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    quantity_kg: float
    price_per_kg: float
    seller_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

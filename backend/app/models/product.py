# backend/app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    quantity_kg = Column(Float)
    price_per_kg = Column(Float)
    seller_id = Column(Integer, index=True)

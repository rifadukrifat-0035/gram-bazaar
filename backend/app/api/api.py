# backend/app/api/api.py
from fastapi import APIRouter
from app.api.endpoints import products, auth, logistics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(products.router, prefix="/market", tags=["Market & AI"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])

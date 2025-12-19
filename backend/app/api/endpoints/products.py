# backend/app/api/endpoints/products.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.schemas.product import Product, ProductCreate
from app.services import stt_service, nlp_service, price_prediction_service
from app.crud import crud_product
from app.db.session import get_db_session

router = APIRouter()

@router.post("/voice-command", response_model=Dict[str, Any])
async def handle_voice_command(
    seller_id: int = Form(1), # Using a default seller_id for MVP
    audio_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session)
):
    """
    This is the core AI endpoint. It orchestrates multiple services:
    1. Transcribes audio to text (STT).
    2. Extracts intent and entities from text (NLP).
    3. Executes the corresponding action (e.g., list a product).
    """
    audio_bytes = await audio_file.read()
    transcribed_text = await stt_service.transcribe_audio(audio_bytes)
    intent_data = await nlp_service.extract_intent(transcribed_text)
    
    if not intent_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not understand the command: '{transcribed_text}'")

    intent = intent_data.get("intent")
    details = intent_data.get("details", {})

    if intent == "SELL_PRODUCT":
        full_details = {**details, "seller_id": seller_id, "category": "produce"}
        product_create = ProductCreate(**full_details)
        new_product = await crud_product.create_product(db=db, product_in=product_create)
        return {"action": "product_listed", "details": new_product}
    
    elif intent == "GET_FORECAST":
        crop_name = details.get("crop_name")
        base_price = 25 # Default price
        forecast = price_prediction_service.generate_mock_forecast(base_price)
        advice = price_prediction_service.get_ai_advice(forecast)
        return {"action": "forecast_generated", "details": {"crop": crop_name, "forecast": forecast, "advice": advice}}

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Command understood, but action is not supported yet.")

@router.get("/", response_model=List[Product])
async def get_all_products(
    db: AsyncSession = Depends(get_db_session), 
    skip: int = 0, 
    limit: int = 20
):
    """
    Get all products with pagination.
    """
    return await crud_product.get_products(db=db, skip=skip, limit=limit)

# backend/app/schemas/auth.py
from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

class OTPSendRequest(BaseModel):
    phone_number: PhoneNumber = Field(..., description="E.164 format phone number")

class OTPVerifyRequest(BaseModel):
    phone_number: PhoneNumber
    otp: str = Field(..., min_length=6, max_length=6)

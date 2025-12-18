# backend/app/api/endpoints/auth.py
from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Depends
from app.schemas.auth import OTPSendRequest, OTPVerifyRequest
from app.services import otp_service
# In a real app, you would have a user CRUD layer here
# from app.crud import crud_user

router = APIRouter()

@router.post("/send-otp", status_code=status.HTTP_202_ACCEPTED)
async def send_otp(request: OTPSendRequest, background_tasks: BackgroundTasks):
    """
    Generates and sends an OTP to the user's phone number.
    The actual SMS sending is deferred to a background task for immediate response.
    """
    phone_str = str(request.phone_number)
    otp = otp_service.generate_and_store_otp(phone_str)
    
    background_tasks.add_task(otp_service.send_otp_via_sms, phone_str, otp)
    
    return {"message": "OTP dispatch initiated."}

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(request: OTPVerifyRequest):
    """
    Verifies the OTP. On success, would typically create a user if they
    don't exist and return a JWT token for session management.
    """
    phone_str = str(request.phone_number)
    if not otp_service.verify_otp(phone_str, request.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP. Please request a new one."
        )
    
    # Here you would typically:
    # 1. Check if user exists: user = await crud_user.get_by_phone(db, phone=phone_str)
    # 2. If not, create user: user = await crud_user.create(db, ...)
    # 3. Create JWT token: access_token = create_access_token(data={"sub": user.id})
    
    return {"message": "OTP verified successfully.", "access_token": "dummy-jwt-for-mvp-testing"}

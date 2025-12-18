# backend/app/services/otp_service.py
import pyotp
from typing import Dict

# In-memory storage for MVP. Use Redis in production.
otp_storage: Dict[str, str] = {}
secret_keys: Dict[str, str] = {}

def generate_and_store_otp(phone_number: str) -> str:
    if phone_number not in secret_keys:
        secret_keys[phone_number] = pyotp.random_base32()
    totp = pyotp.TOTP(secret_keys[phone_number], interval=300) # 5-min validity
    otp = totp.now()
    otp_storage[phone_number] = otp
    return otp

def verify_otp(phone_number: str, user_otp: str) -> bool:
    # This is a simplified verification for the MVP
    stored_otp = otp_storage.get(phone_number)
    if stored_otp and stored_otp == user_otp:
        # Prevent reuse by deleting the OTP after successful verification
        del otp_storage[phone_number]
        return True
    return False

def send_otp_via_sms(phone_number: str, otp: str):
    # Mock function. In production, integrate Twilio or another SMS gateway.
    print(f"--- SIMULATING SENDING OTP ---")
    print(f"To: {phone_number}")
    print(f"Your Gram-Bazaar verification code is: {otp}")
    print(f"----------------------------")

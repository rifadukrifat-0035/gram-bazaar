# backend/app/schemas/logistics.py
from pydantic import BaseModel, Field
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    BOOKED = "booked"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"

class LogisticsRequestCreate(BaseModel):
    origin: str = Field(..., description="Pickup location")
    destination: str = Field(..., description="Drop-off location")
    product_description: str

class JobOffer(BaseModel):
    job_id: int
    origin: str
    destination: str
    product_description: str
    status: JobStatus

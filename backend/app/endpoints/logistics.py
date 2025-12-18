# backend/app/api/endpoints/logistics.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.logistics import LogisticsRequestCreate, JobOffer
from app.services import logistics_service
from typing import List

router = APIRouter()

@router.post("/request-transport", response_model=JobOffer, status_code=status.HTTP_201_CREATED)
async def request_transport(request: LogisticsRequestCreate):
    """

    Creates a new transport request and broadcasts it to available providers.
    """
    new_job = await logistics_service.create_transport_job(
        origin=request.origin,
        destination=request.destination,
        product_description=request.product_description
    )
    return JobOffer(**new_job)

@router.get("/jobs/{job_id}", response_model=JobOffer)
async def get_job_status(job_id: int):
    """
    Get the current status of a specific logistics job.
    """
    job = logistics_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOffer(**job)

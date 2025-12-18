# backend/app/services/logistics_service.py
import asyncio
from typing import Dict, Any

# In-memory database for mock logistics jobs. Use a real DB in production.
MOCK_LOGISTICS_DB: Dict[int, Dict[str, Any]] = {}
JOB_ID_COUNTER = 0

async def create_transport_job(origin: str, destination: str, product_description: str) -> Dict[str, Any]:
    """Creates a new logistics job and simulates broadcasting it."""
    global JOB_ID_COUNTER
    JOB_ID_COUNTER += 1
    job_id = JOB_ID_COUNTER
    
    new_job = {
        "job_id": job_id,
        "origin": origin,
        "destination": destination,
        "product": product_description,
        "status": "PENDING", # PENDING -> BOOKED -> COMPLETED
        "provider_id": None
    }
    MOCK_LOGISTICS_DB[job_id] = new_job
    
    # Simulate broadcasting this job to all nearby drivers
    await broadcast_job_to_providers(job_id, new_job)
    
    return new_job

async def broadcast_job_to_providers(job_id: int, job_details: Dict[str, Any]):
    """Mock service to simulate broadcasting a job to providers via push notifications or WebSockets."""
    print(f"\n--- SIMULATING JOB BROADCAST ---")
    print(f"Broadcasting new job #{job_id} to all available drivers.")
    print(f"Details: From {job_details['origin']} to {job_details['destination']} | Product: {job_details['product']}")
    print("------------------------------\n")
    # In a real app, this would be a call to a WebSocket server or a push notification service.
    await asyncio.sleep(0.5)

def get_job_by_id(job_id: int) -> Dict[str, Any]:
    return MOCK_LOGISTICS_DB.get(job_id)

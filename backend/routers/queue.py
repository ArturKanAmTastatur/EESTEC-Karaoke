"""Queue endpoints — public queue view"""

from typing import List

from fastapi import APIRouter, Depends

from backend import schemas
from backend.routers.songs import get_service
from backend.services import QueueService

router = APIRouter(prefix="/api", tags=["queue"])


@router.get("/queue", response_model=List[schemas.QueueItem])
def get_active_queue(service: QueueService = Depends(get_service)):
    """Return the ordered list of approved songs currently in the queue."""
    # Your code here
    raise NotImplementedError

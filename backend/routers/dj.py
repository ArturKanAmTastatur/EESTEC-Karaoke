"""DJ protected endpoints.

All endpoints under /api/dj/ require the header:

    Authorization: Bearer <DJ_PASSWORD>

The DJ password comes from the environment (KARAOKE_DJ_PASSWORD).
"""

import os
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, status

from backend import schemas
from backend.routers.songs import get_service
from backend.services import QueueService

router = APIRouter(prefix="/api/dj", tags=["dj"])

DJ_PASSWORD = os.environ.get("KARAOKE_DJ_PASSWORD", "111")  # same placeholder as the desktop app


def verify_dj_password(authorization: str = Header(...)) -> None:
    """Validate 'Authorization: Bearer <DJ_PASSWORD>'.

    Raises 401 when the header is missing/malformed and 403 when the
    password is wrong.
    """
    # Your code here
    raise NotImplementedError


@router.post(
    "/updatePendingQueue",
    dependencies=[Depends(verify_dj_password)],
    response_model=schemas.PendingQueueResult,
)
def update_pending_queue(
    body: schemas.PendingQueueAction,
    service: QueueService = Depends(get_service),
):
    """Move a song from pending to the active queue, or reject/remove it."""
    # Your code here
    raise NotImplementedError


@router.post(
    "/updateQueue",
    dependencies=[Depends(verify_dj_password)],
    response_model=List[schemas.QueueItem],
)
def update_queue(
    body: schemas.QueueUpdate,
    service: QueueService = Depends(get_service),
):
    """Update the playback order of the active queue. Returns the updated
    active queue list (same format as GET /api/queue)."""
    # Your code here
    raise NotImplementedError


@router.post(
    "/blacklistUser",
    dependencies=[Depends(verify_dj_password)],
    response_model=schemas.BlacklistResult,
)
def blacklist_user(
    body: schemas.BlacklistRequest,
    service: QueueService = Depends(get_service),
):
    """Ban a userID (and their associated browser_fp) from submitting future
    requests and optionally purge their pending songs."""
    # Your code here
    raise NotImplementedError

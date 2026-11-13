"""Song CRUD routes — guest-facing endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend import schemas
from backend.services import QueueService

router = APIRouter(prefix="/api", tags=["songs"])


def get_service() -> QueueService:
    """QueueService provider — swap for a mock while Component 2 (issue #5)
    is unimplemented."""
    return QueueService()


@router.post(
    "/song",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SongCreated,
    responses={403: {"description": "User is blacklisted from making requests."}},
)
def submit_song_request(
    body: schemas.SongRequestIn,
    service: QueueService = Depends(get_service),
):
    """Create a new User (if browser_fp is new), check blacklist status,
    and add the Song to the Pending Queue (songReq)."""
    # Your code here
    raise NotImplementedError


@router.get(
    "/song/{song_id}",
    response_model=schemas.SongOut,
    responses={404: {"description": "Song not found"}},
)
def get_song(song_id: int, service: QueueService = Depends(get_service)):
    """Get song details by id."""
    # Your code here
    raise NotImplementedError


@router.delete(
    "/song/{song_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Song not found"}},
)
def delete_song(
    song_id: int,
    response: Response,
    service: QueueService = Depends(get_service),
):
    """Delete a song by id."""
    # Your code here
    raise NotImplementedError

"""Shared Pydantic schemas — the API contract.

All components (FastAPI routes, services, frontends) must agree on these
request/response shapes.
"""

from typing import List, Literal

from pydantic import BaseModel

SongStatus = Literal["pending", "queued", "played", "rejected"]


# --- Guest / song endpoints -------------------------------------------------


class SongRequestIn(BaseModel):
    """POST /api/song request body."""

    url: str
    title: str
    browser_fp: str


class SongCreated(BaseModel):
    """POST /api/song 201 response."""

    song_id: int
    userID: str
    status: SongStatus
    message: str


class SongOut(BaseModel):
    """GET /api/song/{song_id} response."""

    id: int
    url: str
    title: str
    userID: str
    status: SongStatus


# --- Queue endpoints ---------------------------------------------------------


class QueueItem(BaseModel):
    """Element of GET /api/queue (and of updateQueue responses)."""

    id: int
    title: str
    url: str
    userID: str


# --- DJ protected endpoints --------------------------------------------------


class PendingQueueAction(BaseModel):
    """POST /api/dj/updatePendingQueue request body."""

    song_id: int
    action: Literal["approve", "reject"]


class PendingQueueResult(BaseModel):
    """POST /api/dj/updatePendingQueue response."""

    status: str
    pending_count: int
    active_queue_count: int


class QueueUpdate(BaseModel):
    """POST /api/dj/updateQueue request body."""

    ordered_song_ids: List[int]


class BlacklistRequest(BaseModel):
    """POST /api/dj/blacklistUser request body."""

    userID: str
    remove_existing_songs: bool = True


class BlacklistResult(BaseModel):
    """POST /api/dj/blacklistUser response."""

    status: Literal["blacklisted"]
    userID: str

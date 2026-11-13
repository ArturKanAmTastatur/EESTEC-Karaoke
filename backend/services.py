"""QueueService — the internal interface between the FastAPI routes and the SQLite database layer.

All methods return plain dicts/lists matching the API contract,
so the routes can be developed against a mocked QueueService while this
class is unimplemented.
"""

from typing import Any, List, Optional


class BlacklistedUserError(Exception):
    """Raised when a browser_fp is blacklisted — maps to 403 Forbidden."""


class QueueService:
    """Business logic for songs, users and the pending/active queues."""

    def create_song_request(self, url: str, title: str, browser_fp: str) -> dict:
        """Create a new User (if browser_fp is new), check blacklist status,
        and add the Song to the Pending Queue.

        Returns:
            {"song_id": int, "userID": str, "status": "pending", "message": str}

        Raises:
            BlacklistedUserError: if browser_fp is blacklisted (maps to 403).
        """
        # Your code here
        raise NotImplementedError

    def get_song(self, song_id: int) -> Optional[dict]:
        """Return the song as {"id", "url", "title", "userID", "status"},
        or None if it does not exist."""
        # Your code here
        raise NotImplementedError

    def delete_song(self, song_id: int) -> bool:
        """Delete the song. Returns True if it existed, False otherwise."""
        # Your code here
        raise NotImplementedError

    def get_active_queue(self) -> List[dict]:
        """Return the ordered list of approved songs currently in the queue:
        [{"id": int, "title": str, "url": str, "userID": str}, ...]"""
        # Your code here
        raise NotImplementedError

    def get_pending_queue(self) -> List[dict]:
        """Return the ordered list of songs awaiting DJ approval
        (same shape as get_active_queue, plus "status": "pending")."""
        # Your code here
        raise NotImplementedError

    def update_pending_queue(self, song_id: int, action: str) -> dict:
        """Move a song from pending to the active queue ("approve"),
        or reject/remove it ("reject").

        Returns:
            {"status": "success", "pending_count": int, "active_queue_count": int}
        """
        # Your code here
        raise NotImplementedError

    def update_active_queue(self, ordered_song_ids: List[int]) -> List[dict]:
        """Update the playback order of the active queue according to
        ordered_song_ids. Returns the updated active queue list
        (same format as get_active_queue)."""
        # Your code here
        raise NotImplementedError

    def blacklist_user(self, user_id: str, remove_songs: bool = True) -> dict:
        """Ban a userID (and their associated browser_fp) from submitting
        future requests and optionally purge their pending songs.

        Returns:
            {"status": "blacklisted", "userID": str}
        """
        # Your code here
        raise NotImplementedError

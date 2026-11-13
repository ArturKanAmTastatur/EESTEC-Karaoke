"""SQLite connection setup and table creation.

Tables:

    users
        userID            TEXT PRIMARY KEY        -- UUID / unique identifier
        browser_fp        TEXT UNIQUE NOT NULL    -- browser fingerprint for rate-limiting/blocking
        is_blacklisted    INTEGER NOT NULL DEFAULT 0

    songs
        id                INTEGER PRIMARY KEY AUTOINCREMENT
        url               TEXT NOT NULL           -- YouTube/Spotify/track URL
        title             TEXT NOT NULL
        userID            TEXT NOT NULL REFERENCES users(userID)
        status            TEXT NOT NULL DEFAULT 'pending'  -- pending | queued | played | rejected
        created_at        TEXT NOT NULL

    queue
        # Need to figure out an implementation and internal schema

Environment:
    KARAOKE_DB_PATH -- path of the SQLite database file (default: karaoke.db)
"""

import os

DB_PATH = os.environ.get("KARAOKE_DB_PATH", "karaoke.db")


def init_db() -> None:
    """Create the users and songs tables above if they do not exist yet."""
    # Your code here
    raise NotImplementedError


def get_connection():
    """Return a new sqlite3 connection to DB_PATH.

    Intended to be used as a context manager, e.g.:

        with get_connection() as conn:
            conn.execute(...)

    """
    # Your code here
    raise NotImplementedError

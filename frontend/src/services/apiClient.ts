/**
 * API client — the single place where the React frontend talks to the
 * FastAPI backend. Implements the `BackendHelpers` contract that App
 * injects into the screen components.
 *
 * Endpoint mapping (see backend/routers/* and backend/schemas.py):
 *   fetchUserSession   -> GET  /api/user/{userId}     (TODO: backend endpoint pending)
 *   createUser         -> POST /api/user              (TODO: backend endpoint pending)
 *   submitSong         -> POST /api/song              (exists: routers/songs.py)
 *   fetchQueueState    -> GET  /api/queue            (exists: routers/queue.py)
 *   checkPendingStatus -> GET  /api/song/{songId}    (exists: routers/songs.py)
 */

import { BackendHelpers, Song, SongDraft } from '../types';

// --- Raw backend shapes (backend/schemas.py) --------------------------------

interface SongOut {
  id: number;
  url: string;
  title: string;
  userID: string;
  status: 'pending' | 'queued' | 'played' | 'rejected';
}

interface QueueItem {
  id: number;
  title: string;
  url: string;
  userID: string;
}

interface SongCreated {
  song_id: number;
  userID: string;
  status: SongOut['status'];
  message: string;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    body: string,
  ) {
    super(`${status}: ${body}`);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    throw new ApiError(res.status, await res.text());
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

// The backend uses lowercase statuses; the frontend contract uses uppercase.
const STATUS_MAP: Record<SongOut['status'], Song['status']> = {
  pending: 'PENDING',
  queued: 'QUEUED',
  played: 'PLAYING',
  rejected: 'REJECTED',
};

function toSong(s: SongOut): Song {
  return {
    id: String(s.id),
    title: s.title,
    url: s.url,
    addedBy: s.userID,
    status: STATUS_MAP[s.status] ?? 'PENDING',
  };
}

export function createApiClient(): BackendHelpers {
  return {
    fetchUserSession: (userId: string) =>
      // TODO(backend): session lookup endpoint pending — must return
      // { user, pendingSong } for the given user id (used by the
      // "New User? - Check local cookie" guard on app initialization).
      request(`/api/user/${encodeURIComponent(userId)}`),

    createUser: (name: string, initialSong?: SongDraft) =>
      // TODO(backend): user creation endpoint pending — must return
      // { user, pendingSong } (used by the onboarding screen).
      request('/api/user', {
        method: 'POST',
        body: JSON.stringify({ name, initialSong }),
      }),

    async submitSong(userId: string, song: SongDraft): Promise<Song> {
      // Existing route POST /api/song expects { url, title, browser_fp }
      // (schemas.SongRequestIn). TODO(design): SongDraft does not carry the
      // song URL / browser fingerprint yet — extend it when AddSongScreen
      // is implemented (screens are intentionally not built out yet).
      const created = await request<SongCreated>('/api/song', {
        method: 'POST',
        body: JSON.stringify({
          url: '',
          title: song.title,
          browser_fp: userId,
        }),
      });
      return {
        id: String(created.song_id),
        title: song.title,
        url: song.url,
        addedBy: created.userID,
        status: STATUS_MAP[created.status] ?? 'PENDING',
      };
    },

    async fetchQueueState(userId: string) {
      const queue = await request<QueueItem[]>('/api/queue');
      const songs: Song[] = queue.map((item) => ({
        id: String(item.id),
        title: item.title,
        url: item.url,
        addedBy: item.userID,
        status: 'QUEUED',
      }));
      // TODO(backend): no "songs by user" endpoint yet — approximate
      // userSongs by filtering the active queue on userID.
      return {
        userSongs: songs.filter((s) => s.addedBy === userId),
        currentQueue: songs,
      };
    },

    async checkPendingStatus(userId: string, songId: string) {
      // Existing route GET /api/song/{song_id}. A blacklisted user is
      // signalled by the backend as HTTP 403 (BlacklistedUserError).
      try {
        const songOut = await request<SongOut>(
          `/api/song/${encodeURIComponent(songId)}`,
        );
        return { isBlacklisted: false, song: toSong(songOut) };
      } catch (err) {
        if (err instanceof ApiError && err.status === 403) {
          return {
            isBlacklisted: true,
            song: {
              id: songId,
              title: '',
              url: '',
              addedBy: userId,
              status: 'REJECTED',
            } satisfies Awaited<
              ReturnType<BackendHelpers['checkPendingStatus']>
            >['song'],
          };
        }
        throw err;
      }
    },
  };
}

/**
 * Shared frontend contracts — single source of truth for the state machine
 * (App.tsx) and the screen components under src/screens/.
 *
 * Screen components rely strictly on these injected interfaces and must not
 * import external API clients or sibling screen modules.
 */

export type Screen =
  | 'INITIALIZING'
  | 'ONBOARDING'
  | 'BLACKLISTED'
  | 'PENDING'
  | 'QUEUE'
  | 'ADD_SONG';

export interface User {
  id: string;
  name: string;
  isBlacklisted: boolean;
}

export interface Song {
  id: string;
  title: string;
  url: string;
  addedBy: string;
  status: 'PENDING' | 'QUEUED' | 'PLAYING' | 'REJECTED';
}

export interface SongDraft {
  title: string;
  url: string;
}

/** Backend helper functions injected by Root App */
export interface BackendHelpers {
  fetchUserSession: (userId: string) => Promise<{
    user: User;
    pendingSong: Song | null;
  }>;
  createUser: (name: string, initialSong?: SongDraft) => Promise<{
    user: User;
    pendingSong: Song | null;
  }>;
  submitSong: (userId: string, song: SongDraft) => Promise<Song>;
  fetchQueueState: (userId: string) => Promise<{
    userSongs: Song[];
    currentQueue: Song[];
  }>;
  checkPendingStatus: (userId: string, songId: string) => Promise<{
    isBlacklisted: boolean;
    song: Song;
  }>;
}

/** State transition mutators injected by Root App */
export interface StateMutators {
  completeOnboarding: (user: User, pendingSong: Song | null) => void;
  markBlacklisted: () => void;
  resolvePendingToQueue: () => void;
  openAddSongForm: () => void;
  completeSongSubmission: (pendingSong: Song) => void;
}

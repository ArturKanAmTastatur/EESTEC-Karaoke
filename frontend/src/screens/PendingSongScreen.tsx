import React from 'react';
import { BackendHelpers, Song, StateMutators, User } from '../types';

export interface PendingSongScreenProps {
  user: User;
  pendingSong: Song;
  checkPendingStatus: BackendHelpers['checkPendingStatus'];
  onApproved: StateMutators['resolvePendingToQueue'];
  onBlacklisted: StateMutators['markBlacklisted'];
}

/**
 * Blue node: "Show Pending Screen" — awaits DJ approval of the pending song.
 *
 * Placeholder — the screen body is intentionally NOT implemented yet.
 */
export const PendingSongScreen: React.FC<PendingSongScreenProps> = () => (
  <main className="screen screen--pending">
    <h1>Waiting for the DJ…</h1>
    <p>Pending song screen — not implemented yet.</p>
  </main>
);

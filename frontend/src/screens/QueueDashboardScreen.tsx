import React from 'react';
import { BackendHelpers, Song, StateMutators, User } from '../types';

export interface QueueDashboardScreenProps {
  user: User;
  userSongs: Song[];
  currentQueue: Song[];
  fetchQueueState: BackendHelpers['fetchQueueState'];
  onSyncQueueData: (userSongs: Song[], currentQueue: Song[]) => void;
  onAddSongClick: StateMutators['openAddSongForm'];
}

/**
 * Blue node: "Show Currently added songs and current queue".
 *
 * Placeholder — the screen body is intentionally NOT implemented yet.
 */
export const QueueDashboardScreen: React.FC<QueueDashboardScreenProps> =
  () => (
    <main className="screen screen--queue">
      <h1>Queue</h1>
      <p>Queue dashboard screen — not implemented yet.</p>
    </main>
  );

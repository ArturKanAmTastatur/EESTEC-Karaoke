import React from 'react';
import { BackendHelpers, StateMutators, User } from '../types';

export interface AddSongScreenProps {
  user: User;
  submitSong: BackendHelpers['submitSong'];
  onSongSubmitted: StateMutators['completeSongSubmission'];
}

/**
 * Blue node: "Add New Song Form".
 *
 * Placeholder — the screen body is intentionally NOT implemented yet.
 */
export const AddSongScreen: React.FC<AddSongScreenProps> = () => (
  <main className="screen screen--add-song">
    <h1>Add a song</h1>
    <p>Add song screen — not implemented yet.</p>
  </main>
);

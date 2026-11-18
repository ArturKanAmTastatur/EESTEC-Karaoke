import React from 'react';

export interface BlacklistedScreenProps {
  userName?: string;
}

/**
 * Blue node: "Blacklisted" — terminal state, no outgoing transitions.
 *
 * Placeholder — the screen body is intentionally NOT implemented yet.
 */
export const BlacklistedScreen: React.FC<BlacklistedScreenProps> = () => (
  <main className="screen screen--blacklisted">
    <h1>🚫 Blacklisted</h1>
    <p>You are not allowed to request songs.</p>
  </main>
);

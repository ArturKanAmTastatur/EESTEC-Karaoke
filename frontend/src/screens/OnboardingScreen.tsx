import React from 'react';
import { BackendHelpers, StateMutators } from '../types';

export interface OnboardingScreenProps {
  createUser: BackendHelpers['createUser'];
  onComplete: StateMutators['completeOnboarding'];
}

/**
 * Blue node: "Ask Name / Create New User in Backend / Additionally let them
 * add a song".
 *
 * Placeholder — the screen body is intentionally NOT implemented yet.
 */
export const OnboardingScreen: React.FC<OnboardingScreenProps> = () => (
  <main className="screen screen--onboarding">
    <h1>EESTEC Karaoke 🎤</h1>
    <p>Onboarding screen — not implemented yet.</p>
  </main>
);

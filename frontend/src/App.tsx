import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Screen,
  User,
  Song,
  BackendHelpers,
  StateMutators,
} from './types';
import { getCookie, setCookie } from './utils/cookies';
import { createApiClient } from './services/apiClient';

// Independent Screen Components (Blue Nodes)
import { OnboardingScreen } from './screens/OnboardingScreen';
import { BlacklistedScreen } from './screens/BlacklistedScreen';
import { PendingSongScreen } from './screens/PendingSongScreen';
import { QueueDashboardScreen } from './screens/QueueDashboardScreen';
import { AddSongScreen } from './screens/AddSongScreen';

const USER_COOKIE_KEY = 'jukebox_user_id';

export const App: React.FC = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>('INITIALIZING');
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [pendingSong, setPendingSong] = useState<Song | null>(null);
  const [userSongs, setUserSongs] = useState<Song[]>([]);
  const [currentQueue, setCurrentQueue] = useState<Song[]>([]);

  // 1. Instantiate backend helpers once to inject into children
  const api: BackendHelpers = useMemo(() => createApiClient(), []);

  // 2. Convergent Decision Guard: Blacklist & "Any Pending Song?"
  const evaluatePostUserGuard = useCallback(
    (user: User, activePendingSong: Song | null) => {
      setCurrentUser(user);
      setPendingSong(activePendingSong);

      if (user.isBlacklisted) {
        setCurrentScreen('BLACKLISTED');
        return;
      }

      if (activePendingSong) {
        setCurrentScreen('PENDING');
      } else {
        setCurrentScreen('QUEUE');
      }
    },
    []
  );

  // 3. Initial Decision Guard: "New User? - Check local cookie"
  useEffect(() => {
    const initializeApp = async () => {
      const existingUserId = getCookie(USER_COOKIE_KEY);

      if (!existingUserId) {
        setCurrentScreen('ONBOARDING');
        return;
      }

      try {
        const { user, pendingSong: existingPending } =
          await api.fetchUserSession(existingUserId);
        evaluatePostUserGuard(user, existingPending);
      } catch {
        // Fallback to onboarding if cookie session is invalid/expired
        setCurrentScreen('ONBOARDING');
      }
    };

    initializeApp();
  }, [api, evaluatePostUserGuard]);

  // 4. State Transition Mutators injected into child screens
  const mutators: StateMutators = useMemo(
    () => ({
      completeOnboarding: (user: User, newPendingSong: Song | null) => {
        setCookie(USER_COOKIE_KEY, user.id);
        evaluatePostUserGuard(user, newPendingSong);
      },
      markBlacklisted: () => {
        setCurrentUser((prev) => (prev ? { ...prev, isBlacklisted: true } : null));
        setCurrentScreen('BLACKLISTED');
      },
      resolvePendingToQueue: () => {
        setPendingSong(null);
        setCurrentScreen('QUEUE');
      },
      openAddSongForm: () => {
        setCurrentScreen('ADD_SONG');
      },
      completeSongSubmission: (newPendingSong: Song) => {
        setPendingSong(newPendingSong);
        setCurrentScreen('PENDING');
      },
    }),
    [evaluatePostUserGuard]
  );

  // 5. Exclusive Screen Renderer
  switch (currentScreen) {
    case 'INITIALIZING':
      return <div className="app-loader">Checking session...</div>;

    case 'ONBOARDING':
      return (
        <OnboardingScreen
          createUser={api.createUser}
          onComplete={mutators.completeOnboarding}
        />
      );

    case 'BLACKLISTED':
      return <BlacklistedScreen userName={currentUser?.name} />;

    case 'PENDING':
      if (!currentUser || !pendingSong) return null;
      return (
        <PendingSongScreen
          user={currentUser}
          pendingSong={pendingSong}
          checkPendingStatus={api.checkPendingStatus}
          onApproved={mutators.resolvePendingToQueue}
          onBlacklisted={mutators.markBlacklisted}
        />
      );

    case 'QUEUE':
      if (!currentUser) return null;
      return (
        <QueueDashboardScreen
          user={currentUser}
          userSongs={userSongs}
          currentQueue={currentQueue}
          fetchQueueState={api.fetchQueueState}
          onSyncQueueData={(songs, queue) => {
            setUserSongs(songs);
            setCurrentQueue(queue);
          }}
          onAddSongClick={mutators.openAddSongForm}
        />
      );

    case 'ADD_SONG':
      if (!currentUser) return null;
      return (
        <AddSongScreen
          user={currentUser}
          submitSong={api.submitSong}
          onSongSubmitted={mutators.completeSongSubmission}
        />
      );
  }
};

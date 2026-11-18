/** Minimal dependency-free cookie helpers for the user session id. */

export function getCookie(key: string): string | null {
  const match = document.cookie
    .split('; ')
    .find((row) => row.startsWith(`${key}=`));
  if (!match) return null;
  return decodeURIComponent(match.slice(key.length + 1));
}

export function setCookie(key: string, value: string): void {
  // No explicit expiry — a session cookie that dies with the browser tab,
  // so guests get a fresh identity on the next event.
  document.cookie = `${encodeURIComponent(key)}=${encodeURIComponent(
    value,
  )}; path=/; samesite=lax`;
}

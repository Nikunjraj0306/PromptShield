import time
from collections import defaultdict, deque
from threading import Lock


class LoginRateLimiter:
    """Blocks repeated failed logins (brute-force protection)."""

    def __init__(self, max_attempts: int = 5, window_seconds: int = 900):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._failures: dict[str, deque] = defaultdict(deque)
        self._lock = Lock()

    def is_blocked(self, key: str) -> int:
        """Return seconds to wait if blocked, or 0 if allowed."""
        now = time.monotonic()

        with self._lock:
            attempts = self._failures.get(key)

            if not attempts:
                return 0

            # Forget failures that are older than the time window.
            while attempts and now - attempts[0] > self.window_seconds:
                attempts.popleft()

            if not attempts:
                del self._failures[key]
                return 0

            if len(attempts) >= self.max_attempts:
                return int(self.window_seconds - (now - attempts[0])) + 1

            return 0

    def record_failure(self, key: str) -> None:
        with self._lock:
            self._failures[key].append(time.monotonic())

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)


login_limiter = LoginRateLimiter()
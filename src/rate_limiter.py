import time
import threading

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        """
        Token bucket rate limiter.

        :param rate: Tokens added per second.
        :param capacity: Max number of tokens allowed in the bucket.
        """
        self.capacity = capacity
        self.tokens = capacity
        self.rate = rate
        self.timestamp = time.monotonic()
        self.lock = threading.Lock()

    def allow_request(self, cost: float = 1.0) -> bool:
        """
        Checks if a request can proceed based on token availability.

        :param cost: Tokens to consume
        :return: True if request is allowed, False otherwise.
        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.timestamp
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.timestamp = now

            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False
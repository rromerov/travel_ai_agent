import unittest
from unittest.mock import patch
from src.rate_limiter import TokenBucket

class TestTokenBucket(unittest.TestCase):

    @patch("src.rate_limiter.time.monotonic")
    def test_initial_allow_request(self, mock_time):
        # Simulate monotonic time
        mock_time.return_value = 1000.0
        bucket = TokenBucket(rate=1.0, capacity=5)

        # First call should succeed and consume 1 token
        self.assertTrue(bucket.allow_request())
        self.assertAlmostEqual(bucket.tokens, 4.0)

    @patch("src.rate_limiter.time.monotonic")
    def test_reject_when_tokens_empty(self, mock_time):
        mock_time.return_value = 1000.0
        bucket = TokenBucket(rate=1.0, capacity=2)

        # Use up all tokens
        self.assertTrue(bucket.allow_request())
        self.assertTrue(bucket.allow_request())
        self.assertFalse(bucket.allow_request())  # No tokens left

    @patch("src.rate_limiter.time.monotonic")
    def test_token_replenishment(self, mock_time):
        mock_time.side_effect = [1000.0, 1000.0, 1002.0]  # Elapsed = 2s

        bucket = TokenBucket(rate=1.0, capacity=2)

        # Use one token at t=1000.0
        self.assertTrue(bucket.allow_request())  # Should reduce to 1 token

        # At t=1002.0, 2s have passed => +2 tokens (max capacity = 2)
        self.assertTrue(bucket.allow_request())  # Should be allowed

    @patch("src.rate_limiter.time.monotonic")
    def test_custom_cost(self, mock_time):
        mock_time.return_value = 1000.0
        bucket = TokenBucket(rate=1.0, capacity=3)

        # Consume with cost=2
        self.assertTrue(bucket.allow_request(cost=2.0))
        self.assertAlmostEqual(bucket.tokens, 1.0)

        # Try to consume more than remaining
        self.assertFalse(bucket.allow_request(cost=2.0))
        self.assertTrue(bucket.allow_request(cost=1.0))

if __name__ == "__main__":
    unittest.main()

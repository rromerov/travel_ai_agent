# tests/test_dependencies.py
import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.dependencies import rate_limiter, token_limiter, request_buckets, token_buckets

class TestRateLimiting(unittest.TestCase):

    def setUp(self):
        # Ensure a clean slate before each test by clearing token buckets
        request_buckets.clear()
        token_buckets.clear()

    @patch("src.dependencies.validate_api_key")
    def test_rate_limiter_allows_request(self, mock_validate):
        # Simulate valid API key
        mock_validate.return_value = {"key": "test-api-key"}
        
        # Mock TokenBucket and allow the request
        with patch("src.dependencies.TokenBucket") as MockBucket:
            mock_bucket = MagicMock()
            mock_bucket.allow_request.return_value = True
            MockBucket.return_value = mock_bucket

            # Should NOT raise any exception since request is allowed
            rate_limiter(api_key_entry=mock_validate.return_value)

            # Ensure the allow_request method was called
            self.assertTrue(mock_bucket.allow_request.called)
            # Verify bucket was stored under the API key
            self.assertIn("test-api-key", request_buckets)

    @patch("src.dependencies.validate_api_key")
    def test_rate_limiter_blocks_request(self, mock_validate):
        # Simulate valid API key
        mock_validate.return_value = {"key": "test-api-key"}

        # Mock TokenBucket and reject the request
        with patch("src.dependencies.TokenBucket") as MockBucket:
            mock_bucket = MagicMock()
            mock_bucket.allow_request.return_value = False
            MockBucket.return_value = mock_bucket

            # Expect HTTP 429 error since the rate limit is exceeded
            with self.assertRaises(HTTPException) as context:
                rate_limiter(api_key_entry=mock_validate.return_value)
            
            # Assert error details match rate limit exceeded
            self.assertEqual(context.exception.status_code, 429)
            self.assertEqual(context.exception.detail, "Request rate limit exceeded.")

    @patch("src.dependencies.validate_api_key")
    def test_token_limiter_returns_bucket(self, mock_validate):
        # Simulate valid API key
        mock_validate.return_value = {"key": "test-api-key"}

        # Mock TokenBucket and capture instance
        with patch("src.dependencies.TokenBucket") as MockBucket:
            mock_instance = MagicMock()
            MockBucket.return_value = mock_instance

            # Should return the mock token bucket
            result = token_limiter(api_key_entry=mock_validate.return_value)

            # Validate returned instance and stored in token_buckets
            self.assertIs(result, mock_instance)
            self.assertIn("test-api-key", token_buckets)

if __name__ == "__main__":
    unittest.main()

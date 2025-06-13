from fastapi import HTTPException, status, Depends
from src.rate_limiter import TokenBucket
from src.api_key import validate_api_key

# Request rate limiting: 5 requests per second
# REQ_RATE = 5
# REQ_CAPACITY = 5
# request_buckets = {}

# To make a quick test, we can decrease the request rate to 1 request per minute per api key
REQ_RATE = 1 / 60  # 1 request per minute
REQ_CAPACITY = 1  # Allow only 1 request at a time
request_buckets = {}

# Token-based rate limiting: 833 tokens/sec
TOKEN_RATE = 833
# Bucket can store up to 5000 tokens, allowing 2 full responses at once
TOKEN_CAPACITY = 5000
token_buckets = {}

def rate_limiter(api_key_entry: dict = Depends(validate_api_key)):
    api_key = api_key_entry["key"]
    if api_key not in request_buckets:
        request_buckets[api_key] = TokenBucket(rate=REQ_RATE, capacity=REQ_CAPACITY)

    if not request_buckets[api_key].allow_request():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Request rate limit exceeded."
        )

def token_limiter(api_key_entry: dict = Depends(validate_api_key)) -> TokenBucket:
    api_key = api_key_entry["key"]
    if api_key not in token_buckets:
        token_buckets[api_key] = TokenBucket(rate=TOKEN_RATE, capacity=TOKEN_CAPACITY)

    return token_buckets[api_key]
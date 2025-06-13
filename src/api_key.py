import json
from fastapi import Header, HTTPException
from pathlib import Path

# Load API keys from JSON file
api_keys_path = Path(__file__).resolve().parent.parent / "data" / "api_keys.json"

with open(api_keys_path) as f:
    api_keys_store = json.load(f)

def validate_api_key(x_api_key: str = Header(...)):
    for entry in api_keys_store:
        if entry["key"] == x_api_key:
            return entry
    raise HTTPException(status_code=403, detail="Invalid API key")

import secrets
import json
from faker import Faker
from pathlib import Path

fake = Faker()

def generate_fake_api_keys(n=10, filename="api_keys.json"):
    """
    Generate a specified number of fake API keys and save them to a JSON file.
    :param n: Number of API keys to generate
    :param filename: Name of the output JSON file
    """
    # Folder to save the mock data
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)  # Create data dir if it doesn't exist
    output_file = data_dir / filename
    # Generate keys
    keys = [
        {
            "key": secrets.token_hex(32),
            "client_name": fake.name()
        }
        for _ in range(n)
    ]
    # Save it as a JSON file
    with output_file.open("w") as f:
        json.dump(keys, f, indent=2)

    print(f"Saved {n} API keys to {output_file}")

if __name__ == "__main__":
    generate_fake_api_keys()
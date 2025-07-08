import requests
import os
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://krivisio-githubcodeuploader.onrender.com"
PROJECT_NAME = "chatbot-test"

# Load from environment
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_USERNAME or not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_USERNAME and GITHUB_TOKEN must be set in .env file")

payload = {
    "name": PROJECT_NAME,
    "structure": [
        {"type": "file", "name": "README.md"},
        {"type": "file", "name": ".gitignore"},
        {
            "type": "folder", "name": "src", "children": [
                {"type": "folder", "name": "main", "children": [{"type": "file", "name": "main.py"}]},
                {"type": "folder", "name": "api", "children": [{"type": "file", "name": "api.py"}]},
                {"type": "folder", "name": "models", "children": []},
                {"type": "folder", "name": "utils", "children": []},
                {"type": "folder", "name": "services", "children": []}
            ]
        },
        {
            "type": "folder", "name": "config", "children": [
                {"type": "file", "name": "config.py"},
                {"type": "file", "name": "settings.py"}
            ]
        },
        {
            "type": "folder", "name": "requirements", "children": [
                {"type": "file", "name": "requirements.txt"}
            ]
        }
    ],
    "github_data": {
        "repo_name": PROJECT_NAME,
        "github_token": GITHUB_TOKEN,
        "github_username": GITHUB_USERNAME
    }
}

def test_create_and_upload():
    print("[*] Sending request to FastAPI backend...")
    response = requests.post(f"{BASE_URL}/create-and-upload", json=payload)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()

    if result["success"]:
        print("[✓] GitHub Upload Successful:", result["message"])
    else:
        print("[✗] GitHub Upload Failed:", result["message"])

if __name__ == "__main__":
    test_create_and_upload()

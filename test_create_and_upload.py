import requests
import os
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://localhost:8000"
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

    # Check if folder structure exists
    assert os.path.exists(PROJECT_NAME), f"Project folder '{PROJECT_NAME}' was not created."

    expected_paths = [
        "README.md", ".gitignore",
        "src/main/main.py", "src/api/api.py",
        "src/models", "src/utils", "src/services",
        "config/config.py", "config/settings.py",
        "requirements/requirements.txt"
    ]

    for rel_path in expected_paths:
        full_path = os.path.join(PROJECT_NAME, rel_path)
        assert os.path.exists(full_path), f"Missing: {rel_path}"

    print("[✓] Folder structure verified.")

    # Clean up
    cleanup = True
    if cleanup:
        shutil.rmtree(PROJECT_NAME)
        print(f"[✓] Cleaned up: {PROJECT_NAME}")

if __name__ == "__main__":
    test_create_and_upload()

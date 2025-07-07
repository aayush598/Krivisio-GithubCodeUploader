import requests

def create_github_repo(repo_name, github_token, github_username):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return {"success": True, "message": "Repository created successfully."}
    elif response.status_code == 422 and "already exists" in response.text:
        return {"success": True, "message": "Repository already exists."}
    else:
        return {"success": False, "message": f"GitHub repo creation failed: {response.text}"}

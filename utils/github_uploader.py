import os
import subprocess
from utils.repo_creator import create_github_repo

BASE_PROJECT_DIR = os.path.abspath(os.getcwd())  # Better path handling

def upload_to_github(project_path, data):
    repo_name = data.get('repo_name')
    github_token = data.get('github_token')
    github_username = data.get('github_username')

    if not repo_name or not github_token or not github_username:
        return {"success": False, "message": "Missing repo name, GitHub token, or GitHub username."}

    # Step 1: Create the GitHub repo via API
    create_repo_result = create_github_repo(repo_name, github_token, github_username)
    if not create_repo_result["success"]:
        return create_repo_result  # Early return if repo creation failed
    
    full_project_path = os.path.join(BASE_PROJECT_DIR, project_path)

    try:
        if not os.path.exists(full_project_path):
            return {"success": False, "message": f"Project path does not exist: {full_project_path}"}

        os.chdir(full_project_path)

        # Step 2: Initialize Git and configure user
        subprocess.run(["git", "init"], check=True)

        subprocess.run(["git", "config", "user.name", github_username], check=True)
        subprocess.run(["git", "config", "user.email", f"{github_username}@users.noreply.github.com"], check=True)

        # Step 3: Add and commit files
        subprocess.run(["git", "add", "."], check=True)

        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status_result.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        # Step 4: Add remote (ensure clean state)
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        repo_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        return {"success": True, "message": "Project uploaded successfully."}

    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Git error: {e.stderr or str(e)}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

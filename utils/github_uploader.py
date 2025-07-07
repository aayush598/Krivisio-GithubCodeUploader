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

    # Create repo first
    create_repo_result = create_github_repo(repo_name, github_token, github_username)
    if not create_repo_result["success"]:
        return create_repo_result  # early return if repo creation failed
    
    full_project_path = os.path.join(BASE_PROJECT_DIR, project_path)

    try:
        if not os.path.exists(full_project_path):
            return {"success": False, "message": f"Project path does not exist: {full_project_path}"}

        os.chdir(full_project_path)

        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)

        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status_result.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        repo_url = f"https://{github_token}@github.com/{github_username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        return {"success": True, "message": "Project uploaded successfully."}

    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Git error: {e}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

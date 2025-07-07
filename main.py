from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from utils.folder_creator import create_project_structure
from utils.github_uploader import upload_to_github
import os

app = FastAPI()

class GitHubData(BaseModel):
    repo_name: str
    github_token: str
    github_username: str

class ProjectRequest(BaseModel):
    name: str
    structure: list
    github_data: GitHubData

@app.post("/create-and-upload")
async def create_and_upload_project(data: ProjectRequest):
    try:
        base_path = os.path.join(os.getcwd(), data.name)
        create_project_structure(base_path, data.structure)
        response = upload_to_github(data.name, data.github_data.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pathlib import Path
from fastapi import FastAPI, HTTPException
from git import Repo
from fastapi import UploadFile, File
from storyteller.parser.js_funcs import extract_function_names
from pydantic import BaseModel
from storyteller.parser.js_diff import diff_functions
import base64

app = FastAPI(title="Git-Storyteller API")
##fetching commits
@app.get("/commits")
def commits(repo: str=".", n: int=10):
    "Return the last n commits from the Git repo located at repo."
    try:
        repo_obj = Repo(Path(repo))
    except Exception as exce:
        raise HTTPException(status_code=400, detail=str(exce))
    
    data = [
        {
            "hash": c.hexsha,
            "author": c.author.name,
            "message": c.message.split("\n")[0],
            "date": c.committed_datetime.isoformat(),
        }
        for c in repo_obj.iter_commits("HEAD",max_count=n)
    ]
    return {"commits": data}

##creating ast by parsing js file and getting function/method names
@app.post("/ast")
async def ast(file: UploadFile=File(...)):
    """
    Upload a javascript file and get its function names.
    """
    source_bytes = await file.read()
    fn_names = extract_function_names(source_bytes)
    return {"functions": fn_names}

class DiffRequest(BaseModel):
    repo: str    #abs or relative path
    path: str    #file within repo
    base: str    #old commit SHA
    head: str    #new commit SHA

@app.post("/diff/ast")
def ast_diff(req: DiffRequest):
    repo = Repo(Path(req.repo))
    #read file at each commit
    old_blob = repo.git.show(f"{req.base}:{req.path}")
    new_blob = repo.git.show(f"{req.head}:{req.path}")
    diff = diff_functions(old_blob.encode(),new_blob.encode())
    return diff
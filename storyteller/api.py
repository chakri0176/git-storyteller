from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from git import Repo
from pydantic import BaseModel
from storyteller.parser.js_funcs import extract_function_names
from storyteller.parser.js_diff import diff_symbols

app = FastAPI(title="Git-Storyteller API")

@app.get("/commits")
def commits(repo: str = ".", n: int = 10):
    """
    Return the last n commits from the Git repo located at repo.
    """
    try:
        repo_obj = Repo(Path(repo))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    commits = [
        {
            "hash": c.hexsha,
            "author": c.author.name,
            "message": c.message.split("\n")[0],
            "date": c.committed_datetime.isoformat(),
        }
        for c in repo_obj.iter_commits("HEAD", max_count=n)
    ]
    return {"commits": commits}

@app.post("/ast")
async def ast(file: UploadFile = File(...)):
    """
    Upload a JavaScript file and get its function names.
    """
    source_bytes = await file.read()
    fn_names = extract_function_names(source_bytes)
    return {"functions": fn_names}

class DiffRequest(BaseModel):
    repo: str    # absolute or relative path to the Git repo
    path: str    # file within the repo
    base: str    # old commit SHA
    head: str    # new commit SHA

@app.post("/diff/ast")
def ast_diff(req: DiffRequest):
    """
    Compare two versions of a file (base vs head) and return added, removed,
    and unchanged symbols (functions, classes, variables).
    """
    try:
        repo = Repo(Path(req.repo))
        old_blob = repo.git.show(f"{req.base}:{req.path}")
        new_blob = repo.git.show(f"{req.head}:{req.path}")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    diff = diff_symbols(old_blob.encode(), new_blob.encode())
    return diff

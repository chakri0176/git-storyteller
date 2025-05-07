from pathlib import Path
from fastapi import FastAPI, HTTPException
from git import Repo

app = FastAPI(title="Git-Storyteller API")

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
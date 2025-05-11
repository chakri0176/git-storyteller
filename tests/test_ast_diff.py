from fastapi.testclient import TestClient
from storyteller.api import app
import tempfile, subprocess, os, textwrap
from pathlib import Path

client = TestClient(app)

def test_ast_diff():
    #creating a tiny temp repo
    with tempfile.TemporaryDirectory() as tdir:
        os.chdir(tdir)
        subprocess.run(["git","init","-q"])
        #commit A
        (Path(tdir)/"demo.js").write_text("function foo() {}")
        subprocess.run(["git","add","demo.js"])
        subprocess.run(["git","commit","-q","-m","A"])
        sha_a = subprocess.check_output(["git","rev-parse","HEAD"]).strip().decode()
        #commit B
        (Path(tdir)/"demo.js").write_text("function foo() {}\nconst bar = () => {}")
        subprocess.run(["git","commit","-am","B","-q"])
        sha_b = subprocess.check_output(["git","rev-parse","HEAD"]).strip().decode()
        
        req_json = {
            "repo": tdir,
            "path": "demo.js",
            "base": sha_a,
            "head": sha_b
        }
        r = client.post("/diff/ast",json = req_json)
        assert r.status_code == 200
        assert r.json() == {"added":["bar"], "removed":[],"unchanged":["foo"]}
        
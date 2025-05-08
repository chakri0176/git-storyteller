from fastapi.testclient import TestClient
from storyteller.api import app

client = TestClient(app)

def test_ast_endpoint():
    code = b"function foo() {}\nconst bar = () => {}"
    resp = client.post("/ast",files={"file":("simple.js",code,"text/javascript")})
    assert resp.status_code == 200
    assert resp.json() == {"functions": ["foo", "bar"]}    
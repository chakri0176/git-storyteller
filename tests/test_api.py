from fastapi.testclient import TestClient
from storyteller.api import app

client = TestClient(app)

def test_commits_endpoint():
    resp = client.get("/commits",params={"n":3})
    assert resp.status_code == 200
    body = resp.json()
    assert "commits" in body
    assert len(body["commits"]) == 3
    #basic sanity check on keys
    keys = {"hash","author","message","date"}
    assert keys.issubset(body["commits"][0].keys())
    
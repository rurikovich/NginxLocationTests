import pytest, requests, json

CASES = [
    ("/api/v1/old-query/items?id=42", "/api/v2/items?id=42"),
    ("/api/v1/old-query/users/alice", "/api/v2/users/alice"),
]

@pytest.mark.parametrize("inp,expected", CASES)
def test_rewrite(inp, expected):
    r = requests.get("http://localhost:8080"+inp, timeout=2)
    data = json.loads(r.text.strip())
    assert r.status_code == 200
    assert data["path"] == expected

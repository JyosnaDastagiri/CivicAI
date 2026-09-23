def test_register(client):
    resp = client.post("/api/auth/register", json={"name": "Alice", "email": "alice@test.com", "password": "Password1"})
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert resp.json()["data"]["user"]["role"] == "CITIZEN"


def test_duplicate_register_fails(client):
    client.post("/api/auth/register", json={"name": "Bob", "email": "bob@test.com", "password": "Password1"})
    resp = client.post("/api/auth/register", json={"name": "Bob2", "email": "bob@test.com", "password": "Password1"})
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/api/auth/register", json={"name": "Carl", "email": "carl@test.com", "password": "Password1"})
    resp = client.post("/api/auth/login", json={"email": "carl@test.com", "password": "Password1"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()["data"]


def test_login_invalid_password(client):
    client.post("/api/auth/register", json={"name": "Dave", "email": "dave@test.com", "password": "Password1"})
    resp = client.post("/api/auth/login", json={"email": "dave@test.com", "password": "WrongPass"})
    assert resp.status_code == 401


def test_protected_route_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401

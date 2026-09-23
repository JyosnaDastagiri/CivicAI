def register_and_login(client, email="citizen1@test.com", password="Password1", name="Test Citizen"):
    client.post("/api/auth/register", json={"name": name, "email": email, "password": password})
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    return resp.json()["data"]["access_token"]

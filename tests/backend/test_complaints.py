from helpers import register_and_login


def _create_complaint(client, token, title="Test pothole", lat=17.38, lon=78.48):
    return client.post(
        "/api/complaints",
        json={
            "title": title, "description": "There is a big pothole causing danger to vehicles.",
            "category": "Pothole", "severity": "HIGH", "safety_risk": True,
            "location": {"latitude": lat, "longitude": lon, "address": "Test Street"},
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_complaint_runs_full_pipeline(client):
    token = register_and_login(client, "complainer1@test.com")
    resp = _create_complaint(client, token)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["status"] in ("ASSIGNED", "AI_ANALYZED")
    assert data["priority"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


def test_complaint_validation_error(client):
    token = register_and_login(client, "complainer2@test.com")
    resp = client.post(
        "/api/complaints",
        json={"title": "a", "description": "x", "category": "Pothole", "location": {"latitude": 1, "longitude": 1}},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


def test_citizen_cannot_view_others_complaint(client):
    token1 = register_and_login(client, "owner@test.com")
    token2 = register_and_login(client, "intruder@test.com")
    resp = _create_complaint(client, token1)
    complaint_id = resp.json()["data"]["id"]
    resp2 = client.get(f"/api/complaints/{complaint_id}", headers={"Authorization": f"Bearer {token2}"})
    assert resp2.status_code == 403

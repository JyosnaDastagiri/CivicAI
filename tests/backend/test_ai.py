from helpers import register_and_login


def test_demo_image_analysis(client):
    token = register_and_login(client, "ai_user@test.com")
    resp = client.post(
        "/api/ai/analyze-image",
        json={"image_url": "http://x/pothole.jpg", "description": "large pothole near gate"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["category"] == "Pothole"
    assert data["severity"] in ("HIGH", "MEDIUM", "LOW", "CRITICAL")


def test_generate_complaint(client):
    token = register_and_login(client, "ai_user2@test.com")
    resp = client.post(
        "/api/ai/generate-complaint",
        json={"citizen_description": "big pothole near gate", "category": "Pothole", "severity": "HIGH", "safety_risk": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "title" in data and "description" in data

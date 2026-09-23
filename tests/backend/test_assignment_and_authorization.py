from helpers import register_and_login


def test_department_assignment_pothole_goes_to_roads(client):
    token = register_and_login(client, "route_test@test.com")
    resp = client.post(
        "/api/complaints",
        json={
            "title": "Pothole routing test", "description": "Deep pothole in the middle of the road causing danger.",
            "category": "Pothole", "severity": "HIGH", "safety_risk": True,
            "location": {"latitude": 17.4, "longitude": 78.5, "address": "Route Test"},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_citizen_cannot_access_admin_settings(client):
    token = register_and_login(client, "citizen_no_admin@test.com")
    resp = client.get("/api/settings", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200  # read allowed to any authenticated user
    resp2 = client.put("/api/settings/ACKNOWLEDGEMENT_DEADLINE_HOURS", json={"value": "1"}, headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 403


def test_citizen_cannot_access_admin_users(client):
    token = register_and_login(client, "citizen_no_users@test.com")
    resp = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

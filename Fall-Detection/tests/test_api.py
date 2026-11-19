import importlib
from fastapi.testclient import TestClient


def test_event_api_lifecycle_and_dashboard(tmp_path, monkeypatch):
    monkeypatch.delenv("CARE_LOOP_API_KEY", raising=False)
    import backend.main as api
    api = importlib.reload(api)

    from backend.database import EventStore
    api.store = EventStore(tmp_path / "api-test.db")
    client = TestClient(api.app)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert "CARE LOOP" in dashboard.text

    created = client.post("/api/v1/events", json={
        "event_type": "FALL_SUSPECTED",
        "severity": "P1",
        "source": "pytest",
        "track_id": 12,
        "metadata": {"detector_state": "FALL_DETECTED"},
    })
    assert created.status_code == 201
    event_id = created.json()["event_id"]

    listed = client.get("/api/v1/events")
    assert listed.status_code == 200
    assert listed.json()["items"][0]["event_id"] == event_id

    acknowledged = client.post(
        f"/api/v1/events/{event_id}/acknowledge",
        json={"actor": "pytest-caregiver"},
    )
    assert acknowledged.status_code == 200
    assert acknowledged.json()["status"] == "ACKNOWLEDGED"

    resolved = client.post(
        f"/api/v1/events/{event_id}/resolve",
        json={"actor": "pytest-caregiver", "note": "Verified safe"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "RESOLVED"

    # Escalation is only valid while an event remains open, so create a second event.
    second = client.post("/api/v1/events", json={
        "event_type": "FALL_SUSPECTED",
        "severity": "P1",
        "source": "pytest",
        "track_id": 13,
    })
    second_id = second.json()["event_id"]
    escalated = client.post(f"/api/v1/events/{second_id}/escalate")
    assert escalated.status_code == 200
    assert escalated.json()["severity"] == "P0"
    assert escalated.json()["event_type"] == "FALL_CONFIRMED"

    audit = client.get(f"/api/v1/events/{event_id}/audit")
    assert audit.status_code == 200
    assert [item["action"] for item in audit.json()["items"]] == [
        "CREATED", "ACKNOWLEDGED", "RESOLVED"
    ]


def test_api_key_guard_rejects_missing_and_accepts_valid_key(tmp_path, monkeypatch):
    monkeypatch.setenv("CARE_LOOP_API_KEY", "test-secret")
    import backend.main as api
    api = importlib.reload(api)

    from backend.database import EventStore
    api.store = EventStore(tmp_path / "auth-test.db")
    client = TestClient(api.app)
    payload = {"event_type": "FALL_SUSPECTED"}

    assert client.post("/api/v1/events", json=payload).status_code == 401
    response = client.post(
        "/api/v1/events",
        json=payload,
        headers={"Authorization": "Bearer test-secret"},
    )
    assert response.status_code == 201

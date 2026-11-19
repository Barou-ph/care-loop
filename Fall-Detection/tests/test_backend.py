from backend.database import EventStore


def make_event(event_id="event-1"):
    return {
        "event_id": event_id,
        "event_type": "FALL_SUSPECTED",
        "severity": "P1",
        "status": "NEW",
        "source": "test",
        "occurred_at": "2026-11-18T10:00:00+00:00",
        "created_at": "2026-11-18T10:00:00+00:00",
        "metadata": {"detector_state": "FALL_DETECTED"},
    }


def test_event_create_and_audit(tmp_path):
    store = EventStore(tmp_path / "test.db")
    event = store.create_event(make_event())
    assert event["status"] == "NEW"
    assert event["metadata"]["detector_state"] == "FALL_DETECTED"
    audit = store.list_audit("event-1")
    assert [item["action"] for item in audit] == ["CREATED"]


def test_acknowledge_then_resolve(tmp_path):
    store = EventStore(tmp_path / "test.db")
    store.create_event(make_event())
    ack = store.transition_event("event-1", "ACKNOWLEDGED", "caregiver-1", None, "2026-11-18T10:01:00+00:00")
    assert ack["acknowledged_by"] == "caregiver-1"
    done = store.transition_event("event-1", "RESOLVED", "caregiver-1", "Checked and safe", "2026-11-18T10:05:00+00:00")
    assert done["status"] == "RESOLVED"
    assert [x["action"] for x in store.list_audit("event-1")] == ["CREATED", "ACKNOWLEDGED", "RESOLVED"]


def test_cannot_resolve_twice(tmp_path):
    store = EventStore(tmp_path / "test.db")
    store.create_event(make_event())
    store.transition_event("event-1", "RESOLVED", "caregiver-1", "done", "2026-11-18T10:05:00+00:00")
    try:
        store.transition_event("event-1", "FALSE_ALARM", "caregiver-1", "false alarm", "2026-11-18T10:06:00+00:00")
    except ValueError:
        pass
    else:
        raise AssertionError("Resolved events must not be transitioned again")



def test_escalate_updates_priority_and_audit(tmp_path):
    store = EventStore(tmp_path / "test.db")
    store.create_event(make_event())
    escalated = store.escalate_event("event-1", "2026-11-18T10:04:00+00:00")
    assert escalated["severity"] == "P0"
    assert escalated["event_type"] == "FALL_CONFIRMED"
    assert escalated["metadata"]["detector_state"] == "CONFIRMED_FALL"
    assert [item["action"] for item in store.list_audit("event-1")] == [
        "CREATED", "ESCALATED"
    ]

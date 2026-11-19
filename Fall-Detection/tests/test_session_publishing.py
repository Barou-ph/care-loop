from app.session import DetectionSession, SessionConfig, SourceKind


class Listener:
    def __init__(self):
        self.alerts = []

    def on_alert(self, event):
        self.alerts.append(event)


class Publisher:
    def __init__(self):
        self.published = []
        self.escalated = []

    def publish_detection_alert(self, alert):
        self.published.append(alert)
        return True

    def publish_escalation(self, alert):
        self.escalated.append(alert)
        return True


def make_alert(state, track_id=7):
    return {
        "track_id": track_id,
        "state": state,
        "features": {"torso_angle": 18.5},
    }


def test_only_one_caregiver_event_is_published_per_fall_episode():
    listener = Listener()
    publisher = Publisher()
    session = DetectionSession(
        SessionConfig(kind=SourceKind.VIDEO, source="unused.mp4", save_path=None),
        listener,
    )
    previous_states = {}

    session._emit_alerts([make_alert("FALL_DETECTED")], previous_states, 1, publisher)
    session._emit_alerts([make_alert("IMPACT")], previous_states, 2, publisher)
    session._emit_alerts([make_alert("CONFIRMED_FALL")], previous_states, 3, publisher)

    assert len(listener.alerts) == 1
    assert len(publisher.published) == 1
    assert len(publisher.escalated) == 1
    assert publisher.escalated[0]["state"] == "CONFIRMED_FALL"

    # Recovery clears the active episode; a later fall on the same track can alert again.
    session._emit_alerts([], previous_states, 4, publisher)
    session._emit_alerts([make_alert("FALL_DETECTED")], previous_states, 5, publisher)
    assert len(listener.alerts) == 2
    assert len(publisher.published) == 2

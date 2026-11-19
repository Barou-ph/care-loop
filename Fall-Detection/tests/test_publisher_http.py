import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backend.publisher import EventPublisher


def test_publisher_posts_event_then_escalates_same_event():
    received = []
    completed = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            received.append((self.path, payload))
            if self.path == "/api/v1/events":
                body = json.dumps({"event_id": "event-123"}).encode()
                self.send_response(201)
            else:
                body = json.dumps({"event_id": "event-123", "severity": "P0"}).encode()
                self.send_response(200)
                completed.set()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    publisher = EventPublisher(f"http://127.0.0.1:{server.server_port}")
    alert = {"track_id": 9, "state": "FALL_DETECTED", "features": {"torso_angle": 18.0}}

    try:
        assert publisher.publish_detection_alert(alert)
        assert publisher.publish_escalation({**alert, "state": "CONFIRMED_FALL"})
        assert completed.wait(3.0)
    finally:
        publisher.close(timeout=2.0)
        server.shutdown()
        server.server_close()
        thread.join(timeout=1.0)

    assert [path for path, _ in received] == [
        "/api/v1/events",
        "/api/v1/events/event-123/escalate",
    ]
    assert received[0][1]["severity"] == "P1"

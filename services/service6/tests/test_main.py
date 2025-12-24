import pytest
from fastapi.testclient import TestClient
from app.main import app, events, counters

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_analytics():
    events.clear()
    counters["total_events"] = 0
    yield
    events.clear()
    counters["total_events"] = 0


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service6"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_log_event():
    r = client.post("/event", json={"event_type": "click", "user_id": "1", "data": "button_id_123"})
    assert r.status_code == 200
    assert r.json()["type"] == "click"
    assert r.json()["user_id"] == "1"


def test_get_stats_empty():
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json()["total_events"] == 0


def test_get_stats():
    client.post("/event", json={"event_type": "click", "user_id": "1"})
    client.post("/event", json={"event_type": "click", "user_id": "2"})
    client.post("/event", json={"event_type": "view", "user_id": "1"})
    
    r = client.get("/stats")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_events"] == 3
    assert stats["by_type"]["click"] == 2
    assert stats["by_type"]["view"] == 1


def test_get_user_events():
    client.post("/event?event_type=click&user_id=1")
    client.post("/event?event_type=view&user_id=1")
    client.post("/event?event_type=click&user_id=2")
    
    r = client.get("/user-events/1")
    assert r.status_code == 200
    assert len(r.json()["events"]) == 2

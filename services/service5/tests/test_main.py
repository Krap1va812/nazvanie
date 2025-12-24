import pytest
from fastapi.testclient import TestClient
from app.main import app, notifications

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_notifs():
    notifications.clear()
    yield
    notifications.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service5"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_send_notification():
    r = client.post("/notify", json={"user_id": "1", "message": "Hello User"})
    assert r.status_code == 200
    assert r.json()["user_id"] == "1"
    assert r.json()["message"] == "Hello User"
    assert r.json()["read"] == False


def test_get_notifications():
    client.post("/notify", json={"user_id": "1", "message": "Message1"})
    client.post("/notify", json={"user_id": "1", "message": "Message2"})
    client.post("/notify", json={"user_id": "2", "message": "Message3"})
    
    r = client.get("/notifications/1")
    assert r.status_code == 200
    assert len(r.json()["notifications"]) == 2


def test_mark_as_read():
    r_create = client.post("/notify", json={"user_id": "1", "message": "Test"})
    notif_id = r_create.json()["id"]
    r = client.put(f"/notifications/{notif_id}/read")
    assert r.status_code == 200
    assert r.json()["read"] == True

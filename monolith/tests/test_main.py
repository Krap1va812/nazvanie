import pytest
from fastapi.testclient import TestClient
from app.main import app, users_db, tasks_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset databases before each test"""
    users_db.clear()
    tasks_db.clear()
    yield
    users_db.clear()
    tasks_db.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["app"] == "monolith"
    assert r.json()["status"] == "ok"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_get_users_empty():
    r = client.get("/users")
    assert r.status_code == 200
    assert r.json()["users"] == []


def test_create_user():
    r = client.post("/users?name=John&email=john@example.com")
    assert r.status_code == 200
    user = r.json()
    assert user["name"] == "John"
    assert user["email"] == "john@example.com"
    assert user["id"] == 1


def test_get_user():
    client.post("/users?name=Jane&email=jane@example.com")
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Jane"


def test_get_user_not_found():
    r = client.get("/users/999")
    assert r.status_code == 404


def test_get_tasks_empty():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json()["tasks"] == []


def test_create_task():
    r = client.post("/tasks?title=Test Task&description=A test task")
    assert r.status_code == 200
    task = r.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "A test task"
    assert task["completed"] == False
    assert task["id"] == 1


def test_get_task():
    client.post("/tasks?title=Another Task")
    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Another Task"


def test_complete_task():
    client.post("/tasks?title=Task to Complete")
    r = client.put("/tasks/1/complete")
    assert r.status_code == 200
    assert r.json()["completed"] == True


def test_stats():
    client.post("/users?name=User1&email=user1@example.com")
    client.post("/users?name=User2&email=user2@example.com")
    client.post("/tasks?title=Task1")
    client.post("/tasks?title=Task2")
    client.put("/tasks/1/complete")
    
    r = client.get("/stats")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_users"] == 2
    assert stats["total_tasks"] == 2
    assert stats["completed_tasks"] == 1

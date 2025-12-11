import pytest
from fastapi.testclient import TestClient
from app.main import app, users_cache

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_users():
    users_cache.clear()
    yield
    users_cache.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service1"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_register_user():
    r = client.post("/register?username=john&age=25")
    assert r.status_code == 200
    assert r.json()["username"] == "john"
    assert r.json()["age"] == 25


def test_register_duplicate():
    client.post("/register?username=john&age=25")
    r = client.post("/register?username=john&age=30")
    assert r.status_code == 400


def test_get_user():
    client.post("/register?username=jane&age=28")
    r = client.get("/users/jane")
    assert r.status_code == 200
    assert r.json()["username"] == "jane"


def test_get_nonexistent_user():
    r = client.get("/users/nonexistent")
    assert r.status_code == 404


def test_count_users():
    r = client.get("/count")
    assert r.status_code == 200
    assert r.json()["total_users"] == 0
    
    client.post("/register?username=alice&age=30")
    client.post("/register?username=bob&age=35")
    
    r = client.get("/count")
    assert r.status_code == 200
    assert r.json()["total_users"] == 2

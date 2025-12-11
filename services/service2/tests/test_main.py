import pytest
from fastapi.testclient import TestClient
from app.main import app, tokens

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tokens():
    tokens.clear()
    yield
    tokens.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service2"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_login_success():
    r = client.post("/login?username=user&password=password123")
    assert r.status_code == 200
    assert "token" in r.json()
    assert r.json()["username"] == "user"


def test_login_invalid_password():
    r = client.post("/login?username=user&password=wrong")
    assert r.status_code == 401


def test_verify_token():
    login_r = client.post("/login?username=user&password=password123")
    token = login_r.json()["token"]
    
    r = client.post(f"/verify?token={token}")
    assert r.status_code == 200
    assert r.json()["valid"] == True


def test_verify_invalid_token():
    r = client.post("/verify?token=invalid_token_12345")
    assert r.status_code == 401


def test_logout():
    login_r = client.post("/login?username=user&password=password123")
    token = login_r.json()["token"]
    
    r = client.post(f"/logout?token={token}")
    assert r.status_code == 200
    
    # Token should be invalid after logout
    r = client.post(f"/verify?token={token}")
    assert r.status_code == 401

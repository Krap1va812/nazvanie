import pytest
from fastapi.testclient import TestClient
from app.main import app, transactions

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_txns():
    transactions.clear()
    yield
    transactions.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service3"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_process_payment():
    r = client.post("/pay", json={"user_id": "1", "amount": 100.50})
    assert r.status_code == 200
    assert r.json()["user_id"] == "1"
    assert r.json()["amount"] == 100.50
    assert r.json()["status"] == "completed"


def test_invalid_amount():
    r = client.post("/pay", json={"user_id": "1", "amount": -50})
    assert r.status_code == 400


def test_get_transaction():
    client.post("/pay", json={"user_id": "1", "amount": 50})
    r = client.get("/transaction/1")
    assert r.status_code == 200
    assert r.json()["amount"] == 50


def test_get_transaction_not_found():
    r = client.get("/transaction/999")
    assert r.status_code == 404


def test_get_balance():
    client.post("/pay?user_id=1&amount=100")
    client.post("/pay?user_id=1&amount=50")
    client.post("/pay?user_id=2&amount=75")
    
    r = client.get("/balance/1")
    assert r.status_code == 200
    assert r.json()["total_paid"] == 150
    
    r = client.get("/balance/2")
    assert r.status_code == 200
    assert r.json()["total_paid"] == 75

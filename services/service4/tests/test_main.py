import pytest
from fastapi.testclient import TestClient
from app.main import app, products

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_products():
    products.clear()
    yield
    products.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "service4"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_create_product():
    r = client.post("/products", json={"name": "Laptop", "price": 999.99, "stock": 10})
    assert r.status_code == 200
    assert r.json()["name"] == "Laptop"
    assert r.json()["price"] == 999.99
    assert r.json()["stock"] == 10


def test_create_invalid_product():
    r = client.post("/products", json={"name": "Phone", "price": -50, "stock": 5})
    assert r.status_code == 400


def test_get_product():
    client.post("/products", json={"name": "Mouse", "price": 25.99, "stock": 100})
    r = client.get("/products/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Mouse"


def test_list_products():
    client.post("/products", json={"name": "Item1", "price": 10, "stock": 5})
    client.post("/products", json={"name": "Item2", "price": 20, "stock": 10})
    
    r = client.get("/products")
    assert r.status_code == 200
    assert len(r.json()["products"]) == 2


def test_update_stock():
    client.post("/products", json={"name": "Book", "price": 15.99, "stock": 50})
    r = client.put("/products/1/stock", json={"quantity": 30})
    assert r.status_code == 200
    assert r.json()["stock"] == 30

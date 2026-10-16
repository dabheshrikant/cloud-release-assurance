from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_readiness_endpoint():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_create_and_retrieve_order():
    create = client.post("/orders", json={"item": "keyboard", "quantity": 2})
    assert create.status_code == 201
    order = create.json()
    assert order["item"] == "keyboard"
    assert order["quantity"] == 2
    assert order["status"] == "created"

    read = client.get(f'/orders/{order["id"]}')
    assert read.status_code == 200
    assert read.json()["id"] == order["id"]

def test_reject_invalid_quantity():
    response = client.post("/orders", json={"item": "keyboard", "quantity": 0})
    assert response.status_code == 422

def test_unknown_order_returns_404():
    response = client.get("/orders/does-not-exist")
    assert response.status_code == 404

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(title="Cloud Release Assurance Orders API", version="0.1.0")

class OrderIn(BaseModel):
    item: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0, le=1000)

class Order(OrderIn):
    id: str
    status: str = "created"

_orders: dict[str, Order] = {}

@app.get("/health")
def health():
    # Liveness: the process is running.
    return {"status": "ok"}

@app.get("/ready")
def ready():
    # Starter example has no external dependencies; extend when adding a database.
    return {"status": "ready"}

@app.post("/orders", response_model=Order, status_code=201)
def create_order(payload: OrderIn):
    order = Order(id=str(uuid4()), item=payload.item, quantity=payload.quantity)
    _orders[order.id] = order
    return order

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = _orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

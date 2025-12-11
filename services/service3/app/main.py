from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Service 3 - Payment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transactions = {}

class PaymentRequest(BaseModel):
    user_id: str
    amount: float


@app.get("/")
def root():
    return {"service": "service3", "name": "Payment Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service3"}


@app.post("/pay")
def process_payment(data: PaymentRequest):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    txn_id = len(transactions) + 1
    transaction = {
        "id": txn_id,
        "user_id": data.user_id,
        "amount": data.amount,
        "status": "completed"
    }
    transactions[txn_id] = transaction
    return transaction


@app.get("/transaction/{txn_id}")
def get_transaction(txn_id: int):
    if txn_id not in transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transactions[txn_id]


@app.get("/balance/{user_id}")
def get_balance(user_id: str):
    total = sum(t["amount"] for t in transactions.values() if str(t["user_id"]) == user_id)
    return {"user_id": user_id, "total_paid": total}

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Service 4 - Product Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = {}

class CreateProductRequest(BaseModel):
    name: str
    price: float
    stock: int

class UpdateStockRequest(BaseModel):
    quantity: int


@app.get("/")
def root():
    return {"service": "service4", "name": "Product Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service4"}


@app.post("/products")
def create_product(data: CreateProductRequest):
    if data.price <= 0 or data.stock < 0:
        raise HTTPException(status_code=400, detail="Invalid price or stock")
    
    product_id = len(products) + 1
    product = {
        "id": product_id,
        "name": data.name,
        "price": data.price,
        "stock": data.stock
    }
    products[product_id] = product
    return product


@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]


@app.get("/products")
def list_products():
    return {"products": list(products.values())}


@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, data: UpdateStockRequest = Body(...)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id]["stock"] = data.quantity
    return products[product_id]

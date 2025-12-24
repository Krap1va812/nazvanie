from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Service 1 - User Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_cache = {}

class RegisterRequest(BaseModel):
    username: str
    age: int = 0


@app.get("/")
def root():
    return {"service": "service1", "name": "User Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service1"}


@app.post("/register")
def register_user(data: RegisterRequest):
    if data.username in users_cache:
        raise HTTPException(status_code=400, detail="User already exists")
    user = {"username": data.username, "age": data.age}
    users_cache[data.username] = user
    return user


@app.get("/users/{username}")
def get_user(username: str):
    if username not in users_cache:
        raise HTTPException(status_code=404, detail="User not found")
    return users_cache[username]


@app.get("/count")
def count_users():
    return {"total_users": len(users_cache)}

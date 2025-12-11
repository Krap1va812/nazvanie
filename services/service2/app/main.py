from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets

app = FastAPI(title="Service 2 - Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}  # {username: password}
tokens = {}    # {token: username}

class LoginRequest(BaseModel):
    username: str
    password: str

class VerifyRequest(BaseModel):
    token: str

class LogoutRequest(BaseModel):
    token: str

class RegisterRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"service": "service2", "name": "Auth Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service2"}


@app.post("/register")
def register_user(data: RegisterRequest):
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[data.username] = data.password
    return {"username": data.username, "message": "User registered successfully"}


@app.post("/login")
def login(data: LoginRequest):
    if data.username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    if users_db[data.username] != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    token = secrets.token_hex(16)
    tokens[token] = data.username
    return {"token": token, "username": data.username}


@app.post("/verify")
def verify_token(data: VerifyRequest):
    if data.token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"valid": True, "username": tokens[data.token]}


@app.post("/logout")
def logout(data: LogoutRequest):
    if data.token in tokens:
        del tokens[data.token]
    return {"status": "logged out"}

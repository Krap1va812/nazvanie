from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Monolith App", version="1.0.0")

# CORS для микросервисов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы (HTML, CSS, JS)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# In-memory storage
users_db = {}
tasks_db = {}


@app.get("/")
def root():
    return {
        "app": "monolith",
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/index.html")
def index():
    return FileResponse(str(static_dir / "index.html"))


@app.get("/ui")
def ui():
    return FileResponse(str(static_dir / "index.html"))


@app.get("/health")
def health():
    return {"status": "healthy", "service": "monolith"}


@app.get("/users")
def get_users():
    return {"users": list(users_db.values())}


@app.post("/users")
def create_user(name: str, email: str):
    user_id = len(users_db) + 1
    user = {"id": user_id, "name": name, "email": email}
    users_db[user_id] = user
    return user


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.get("/tasks")
def get_tasks():
    return {"tasks": list(tasks_db.values())}


@app.post("/tasks")
def create_task(title: str, description: str = ""):
    task_id = len(tasks_db) + 1
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    tasks_db[task_id] = task
    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id]["completed"] = True
    return tasks_db[task_id]


@app.get("/stats")
def stats():
    return {
        "total_users": len(users_db),
        "total_tasks": len(tasks_db),
        "completed_tasks": sum(1 for t in tasks_db.values() if t["completed"])
    }

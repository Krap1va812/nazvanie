from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Service 5 - Notification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

notifications = {}

class NotificationRequest(BaseModel):
    user_id: str
    message: str


@app.get("/")
def root():
    return {"service": "service5", "name": "Notification Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service5"}


@app.post("/notify")
def send_notification(data: NotificationRequest):
    notification_id = len(notifications) + 1
    notification = {
        "id": notification_id,
        "user_id": data.user_id,
        "message": data.message,
        "sent_at": datetime.utcnow().isoformat(),
        "read": False
    }
    notifications[notification_id] = notification
    return notification


@app.get("/notifications/{user_id}")
def get_notifications(user_id: str):
    user_notifs = [n for n in notifications.values() if str(n["user_id"]) == user_id]
    return {"notifications": user_notifs}


@app.put("/notifications/{notif_id}/read")
def mark_as_read(notif_id: int):
    if notif_id not in notifications:
        raise HTTPException(status_code=404, detail="Notification not found")
    notifications[notif_id]["read"] = True
    return notifications[notif_id]

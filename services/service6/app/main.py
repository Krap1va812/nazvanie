from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Service 6 - Analytics Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

events = {}
counters = {"total_events": 0}

class EventRequest(BaseModel):
    event_type: str
    user_id: str
    data: str = ""


@app.get("/")
def root():
    return {"service": "service6", "name": "Analytics Service", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "service6"}


@app.post("/event")
def log_event(event_data: EventRequest):
    event_id = len(events) + 1
    event = {
        "id": event_id,
        "type": event_data.event_type,
        "user_id": event_data.user_id,
        "data": event_data.data
    }
    events[event_id] = event
    counters["total_events"] += 1
    return event


@app.get("/stats")
def get_stats():
    event_types = {}
    for event in events.values():
        event_type = event["type"]
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    return {
        "total_events": counters["total_events"],
        "by_type": event_types
    }


@app.get("/user-events/{user_id}")
def get_user_events(user_id: str):
    user_events = [e for e in events.values() if str(e["user_id"]) == user_id]
    return {"user_id": user_id, "events": user_events}

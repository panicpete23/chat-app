# app/main.py
from __future__ import annotations
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .db import init_db, get_db, Message

app = FastAPI(title="Chat App Starter", version="0.1.0")

# CORS (allow local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

# Simple index route to the UI
@app.get("/")
def index():
    return FileResponse("static/index.html")

# ---- REST: fetch recent messages ----
class MessageOut(BaseModel):
    id: int
    username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/api/messages", response_model=List[MessageOut])
def get_messages(limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Message).order_by(Message.id.desc()).limit(limit).all()
    # return newest->oldest by id desc; frontend can reverse if desired
    return list(reversed(q))

# ---- WebSocket chat ----
@dataclass
class Connection:
    websocket: WebSocket
    username: str

class Hub:
    def __init__(self):
        self.connections: Set[Connection] = set()

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.connections.add(Connection(websocket, username))

    def _by_ws(self, websocket: WebSocket) -> Connection | None:
        for c in self.connections:
            if c.websocket is websocket:
                return c
        return None

    def disconnect(self, websocket: WebSocket):
        conn = self._by_ws(websocket)
        if conn:
            self.connections.remove(conn)

    async def broadcast(self, payload: dict):
        # send to everyone; drop failed connections silently
        stale: list[Connection] = []
        text = json.dumps(payload, default=str)
        for c in list(self.connections):
            try:
                await c.websocket.send_text(text)
            except:  # noqa: E722
                stale.append(c)
        for c in stale:
            self.connections.discard(c)

hub = Hub()

class Inbound(BaseModel):
    username: str = Field(..., max_length=50)
    content: str = Field(..., max_length=1000)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    # Expect a query param ?username=YourName or the client sends a hello
    username = websocket.query_params.get("username", "Guest")
    await hub.connect(websocket, username)

    # Announce join (ephemeral)
    join_evt = {"type": "system", "event": "join", "username": username, "created_at": datetime.utcnow().isoformat()} 
    await hub.broadcast(join_evt)

    try:
        while True:
            raw = await websocket.receive_text()
            data = Inbound.model_validate_json(raw)

            # Persist message
            msg = Message(username=data.username, content=data.content)
            db.add(msg)
            db.commit()
            db.refresh(msg)

            # Broadcast to all
            outgoing = {
                "type": "message",
                "id": msg.id,
                "username": msg.username,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            await hub.broadcast(outgoing)

    except WebSocketDisconnect:
        hub.disconnect(websocket)
        leave_evt = {"type": "system", "event": "leave", "username": username, "created_at": datetime.utcnow().isoformat()}
        await hub.broadcast(leave_evt)

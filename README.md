# Chat App Starter — FastAPI + WebSocket

A minimal yet practical chat app: FastAPI backend with WebSockets, SQLite message history, and a tiny vanilla HTML/JS client.

## Features
- Realtime chat over WebSocket (`/ws`)
- Message history via REST (`/api/messages`)
- SQLite persistence (no setup)
- Static frontend served from the same app

## Quickstart
```bash
python -m venv .venv
# Windows:  . .venv/Scripts/activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Deploy notes
- **Docker**: Add a Dockerfile if you want containerized deploy.
- **Prod server**: Use `uvicorn` or `gunicorn` with `uvicorn.workers.UvicornWorker` behind a reverse proxy.
- **HTTPS**: In production, terminate TLS at your proxy and the client will use `wss://` automatically.

## Roadmap (good first issues)
- [ ] Username prompt + lightweight auth token
- [ ] "Typing…" indicators
- [ ] Rooms/channels (e.g., `/ws/general`, `/ws/random`)
- [ ] Rate‑limit & moderation hooks
- [ ] Export/download chat history
- [ ] Dark/light theme toggle

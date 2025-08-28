# Chat App Starter — FastAPI + WebSocket

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-teal.svg)](https://fastapi.tiangolo.com/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **beginner-friendly real-time chat application** built with **FastAPI**, **WebSockets**, and **SQLite**.  
Designed as a starter project to explore real-time apps, WebSocket communication, and lightweight persistence.  

---

## 🚀 Features
- 🔌 **WebSocket chat**: Send/receive messages in real-time.  
- 💾 **SQLite persistence**: Messages are stored locally in a simple DB.  
- 📜 **Message history API**: Fetch past chat logs via REST.  
- 🎨 **Minimal frontend**: Plain HTML + JavaScript, no build tools.  
- 🐳 **Docker-ready**: Included `Dockerfile` for easy containerization.  

---

## 📸 Demo Screenshot
>Coming Soon  

---

## ⚡ Quickstart

```bash
# Clone the repo
git clone https://github.com/panicpete23/chat-app.git
cd chat-app

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Open in browser:
# http://127.0.0.1:8000


🧰 Tech Stack
FastAPI — modern async Python framework
WebSockets — real-time communication
SQLite — lightweight database
Vanilla JS — simple frontend

🛣 Roadmap
 Add multiple chat rooms/channels
 Add user authentication (JWT or simple login)
 Add “typing…” indicators
 Add dark/light mode toggle
 Export chat history as CSV/JSON
 Deploy to Render / Fly.io / Heroku

📜 License
This project is licensed under the MIT License.

💡 Why This Project?
I built this as my first real chat app to strengthen my skills in:
WebSockets & real-time communication
API design with FastAPI
Using databases in small projects
Structuring a portfolio-ready Python project
👋 If you like this project, feel free to star ⭐ the repo or fork it for your own experiments!

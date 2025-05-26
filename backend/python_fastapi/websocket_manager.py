# websocket_manager.py
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        print("initialized connection manager")
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_progress(self, message: dict):
        for connection in self.active_connections:
            print("sending message to connection")
            await connection.send_json(message)

manager = ConnectionManager()

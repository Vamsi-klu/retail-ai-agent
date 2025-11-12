"""WebSocket support for real-time updates."""
from app.websocket.manager import ConnectionManager
from app.websocket.events import WebSocketEventType

__all__ = ["ConnectionManager", "WebSocketEventType"]

"""
WebSocket endpoints for real-time communication.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket.manager import manager
from app.core.security import verify_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates.

    Accepts connections and handles real-time event streaming.
    """
    user_id = None

    # Try to authenticate from query parameters
    token = websocket.query_params.get("token")
    if token:
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")
        except Exception as e:
            logger.warning(f"WebSocket authentication failed: {e}")

    await manager.connect(websocket, user_id)

    try:
        # Send welcome message
        await manager.send_personal_message(
            {"type": "connected", "message": "WebSocket connection established"},
            websocket
        )

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_json()

            # Echo received data (can be extended for client commands)
            await manager.send_personal_message(
                {"type": "echo", "data": data},
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)

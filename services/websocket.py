# -*- coding: utf-8 -*-
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
router = APIRouter(tags=["Sovereign Real-Time WebSocket"])
@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Sovereign Echo: {data}")
    except WebSocketDisconnect:
        pass

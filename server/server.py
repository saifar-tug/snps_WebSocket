"""
server.py
Async WebSocket server exposing a simple computation function.

The server:
- Accepts a persistent WebSocket connection.
- Receives JSON messages containing a function name and arguments.
- Routes the request to a computation function (multiply_numbers).
- Returns the computed result or a structured error.
- Maintains an open connection for multiple requests.

This pattern is a simplified version of an AI control layer:
structured messages -> validated -> executed -> structured response.
"""

import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Any, Dict

from .operations import multiply_numbers


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Main WebSocket endpoint.
    Receives JSON payloads and returns computed results.

    Expected client message format:
    {
        "func": "multiply",
        "args": [3, 4]
    }

    Server response:
    {
        "result": 12
    }
    """
    await websocket.accept()

    while True:
        try:
            # Receive raw text message
            data_str = await websocket.receive_text()

            # Parse JSON
            try:
                payload: Dict[str, Any] = json.loads(data_str)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
                continue

            # Validate request structure
            if "func" not in payload or "args" not in payload:
                await websocket.send_json({
                    "error": "Message must contain 'func' and 'args'"
                })
                continue

            func_name = payload["func"]
            args = payload["args"]

            # Route to server function
            if func_name == "multiply":
                try:
                    result = multiply_numbers(*args)
                    await websocket.send_json({"result": result})
                except Exception as e:
                    await websocket.send_json({"error": str(e)})

            else:
                await websocket.send_json({
                    "error": f"Unknown function '{func_name}'"
                })

        except WebSocketDisconnect:
            print("Client disconnected")
            break

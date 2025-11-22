"""
client.py
Async WebSocket client that calls server functions using websocket-client.

We use websocket-client instead of the 'websockets' library to maintain
compatibility with FastAPI's ASGI WebSocket implementation, especially on macOS.
To preserve the async interface required by the exercise, the blocking send/recv
operations run inside a thread executor.

This matches how AI systems send structured compute requests to an AI Control Layer.
"""

import asyncio
import json
from typing import Any, Dict
from websocket import create_connection, WebSocketException


SERVER_URL = "ws://localhost:8000/ws"


async def call_multiply(a: float, b: float) -> float:
    """
    Asynchronously call the server's multiply function.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: The computed result from the server.

    Raises:
        RuntimeError: If the server returns an error field or if the connection fails.
    """

    loop = asyncio.get_running_loop()

    def send_and_receive() -> Dict[str, Any]:
        try:
            # Connect (blocking)
            ws = create_connection(SERVER_URL)

            # Send request
            request = {"func": "multiply", "args": [a, b]}
            ws.send(json.dumps(request))

            # Receive response
            response_raw = ws.recv()
            ws.close()

            # Parse JSON
            return json.loads(response_raw)

        except (ConnectionRefusedError, WebSocketException) as exc:
            # Give a clearer error message for debugging or logs
            raise RuntimeError(f"Failed to contact server: {exc}")

    # Run blocking WS code in a separate thread so this remains async
    response: Dict[str, Any] = await loop.run_in_executor(None, send_and_receive)

    # Handle server-side errors
    if "error" in response:
        raise RuntimeError(response["error"])

    # Normal successful path
    return float(response["result"])


async def demo_multiple_calls() -> None:
    """
    Demonstrate multiple async calls over independent WebSocket connections.
    Each call is awaited sequentially for clarity in logs.
    """
    print("Connected to server. Sending requests...\n")

    test_values = [(3, 4), (10, 8), (-5, 3)]

    for a, b in test_values:
        result = await call_multiply(a, b)
        print(f"{a} * {b} = {result}")


if __name__ == "__main__":
    asyncio.run(demo_multiple_calls())

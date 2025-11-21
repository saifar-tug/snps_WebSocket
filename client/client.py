"""
client.py
Async WebSocket client that calls server functions.

This client:
- Opens a WebSocket connection
- Sends structured JSON requests to the server
- Awaits async responses
- Prints results
- Demonstrates multiple calls over one persistent connection

This matches how AI systems send structured compute requests
to an AI Control Layer.
"""

import asyncio
import json
import websockets
from typing import Any, Dict


async def call_multiply(a: float, b: float) -> float:
    """
    Send a multiply request to the server and return the result.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: Server result.

    Raises:
        RuntimeError: If the server returns an error.
    """

    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Send JSON request
        request = {"func": "multiply", "args": [a, b]}
        await websocket.send(json.dumps(request))

        # Await server response
        response_str = await websocket.recv()
        response: Dict[str, Any] = json.loads(response_str)

        # Error handling
        if "error" in response:
            raise RuntimeError(response["error"])

        return response["result"]


async def demo_multiple_calls() -> None:
    """Demonstrate multiple async calls to the server."""
    print("Connected to server. Sending requests...\n")

    values = [(3, 4), (10, 8), (-5, 3)]

    for a, b in values:
        result = await call_multiply(a, b)
        print(f"{a} * {b} = {result}")


if __name__ == "__main__":
    asyncio.run(demo_multiple_calls())

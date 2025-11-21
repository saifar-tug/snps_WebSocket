import asyncio
import pytest
import websockets
import json
from server.operations import multiply_numbers


@pytest.mark.asyncio
async def test_e2e_multiply():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        await websocket.send(json.dumps({"func": "multiply", "args": [3, 4]}))
        response = json.loads(await websocket.recv())
        assert response["result"] == 12.0

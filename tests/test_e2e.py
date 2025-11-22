import json
from websocket import create_connection

def test_e2e_multiply():
    """
    End-to-end test using websocket-client.

    Ensures the WebSocket server accepts a request,
    routes it to multiply_numbers, and returns the correct result.
    """
    ws = create_connection("ws://localhost:8000/ws")

    # Send request
    ws.send(json.dumps({"func": "multiply", "args": [3, 4]}))

    # Receive response
    response = json.loads(ws.recv())
    ws.close()

    assert response["result"] == 12.0

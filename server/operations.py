"""
operations.py
Core computation functions for the WebSocket server.
These functions are intentionally pure and stateless so they can be:
- independently tested,
- reused cleanly,
- decoupled from WebSocket / network logic.

This mirrors patterns used in AI Control Layers, where computation
is abstracted from communication.
"""

from typing import Union


def multiply_numbers(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Multiply two numbers and return the result.

    Args:
        a (int | float): First number.
        b (int | float): Second number.

    Returns:
        float: Product of a and b.

    Raises:
        TypeError: If a or b is not numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("multiply_numbers expects two numeric values")

    return float(a * b)

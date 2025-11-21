from server.operations import multiply_numbers
import pytest


def test_multiply_numbers_basic():
    assert multiply_numbers(3, 4) == 12.0
    assert multiply_numbers(10, 0) == 0.0


def test_multiply_numbers_negative():
    assert multiply_numbers(-5, 3) == -15.0


def test_multiply_numbers_invalid():
    with pytest.raises(TypeError):
        multiply_numbers("a", 5)

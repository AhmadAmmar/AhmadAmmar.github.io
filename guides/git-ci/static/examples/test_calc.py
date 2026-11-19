"""Tests check the code against answers worked out by hand. Run: python -m pytest"""
import pytest

from calc import heat_loss


def test_known_answer():
    """U 2.1 W/m2K x 10 m2 x 15 K = 315 W, worked by hand."""
    assert heat_loss(2.1, 10, 15) == pytest.approx(315)


def test_no_temperature_difference_means_no_loss():
    """No temperature difference, no heat loss."""
    assert heat_loss(2.1, 10, 0) == 0


def test_impossible_input_is_refused():
    """An impossible input raises ValueError."""
    with pytest.raises(ValueError):
        heat_loss(-1, 10, 15)

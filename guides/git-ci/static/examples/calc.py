"""A tiny calculation to test."""


def heat_loss(u, area, delta_t):
    """Heat loss in watts: Q = U A dT."""
    if u < 0 or area < 0:
        raise ValueError("U-value and area cannot be negative")
    return u * area * delta_t

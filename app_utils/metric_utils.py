"""Formatting helpers for app metrics."""

from __future__ import annotations


def format_percent(value: object, digits: int = 1) -> str:
    """Format a decimal value as a percentage."""

    number = _to_float(value)
    if number is None:
        return "n/a"
    return f"{number * 100:.{digits}f}%"


def format_count(value: object) -> str:
    """Format a count value with thousands separators."""

    number = _to_float(value)
    if number is None:
        return "n/a"
    return f"{int(round(number)):,}"


def format_metric(value: object, digits: int = 3) -> str:
    """Format a numeric metric value."""

    number = _to_float(value)
    if number is None:
        return "n/a"
    return f"{number:.{digits}f}"


def format_threshold(value: object) -> str:
    """Format a model threshold value."""

    return format_metric(value, digits=3)


def format_cost(value: object) -> str:
    """Format an illustrative cost value."""

    number = _to_float(value)
    if number is None:
        return "n/a"
    return f"{number:,.2f}"


def _to_float(value: object) -> float | None:
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None

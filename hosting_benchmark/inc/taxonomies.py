"""Hosting benchmark taxonomies."""
from typing import NamedTuple


class BenchmarkResult(NamedTuple):
    """Single benchmark result."""

    timestamp: float
    number: int
    data: dict

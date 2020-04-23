from typing import NamedTuple


class BenchmarkResult(NamedTuple):
    timestamp: float
    number: int
    data: dict

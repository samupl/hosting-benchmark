from statistics import mean
from typing import Dict, Iterable

from terminaltables import SingleTable

from hosting_benchmark.inc.formatters import format_timing
from hosting_benchmark.inc.taxonomies import BenchmarkResult


def get_timings(results: Iterable[BenchmarkResult], key: str):
    return [
        result.data[key]['timeTaken'] for result in results
    ]


def calculate_timing_stats(timings: Iterable[float]) -> Dict[str, float]:
    return {
        'min': min(timings),
        'max': max(timings),
        'mean': mean(timings),
        'total': sum(timings),
    }


def render_table(result):
    table = SingleTable(
        table_data=[
                       ['Name', 'Min', 'Max', 'Mean', 'Total'],
                   ] + [
                       [
                           key,
                       ] + [
                           format_timing(result['timings'][key][inner_key])
                           for inner_key in ['min', 'max', 'mean', 'total']
                       ]
                       for key, value in result['timings'].items()
                   ]
    )
    return table.table

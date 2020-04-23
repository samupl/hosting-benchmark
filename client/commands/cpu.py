import time
from statistics import mean
from typing import NamedTuple

import click
import requests
from terminaltables import SingleTable

from inc.formatters import format_timing


class CPUBenchmarkResult(NamedTuple):
    timestamp: float
    number: int
    data: dict


@click.command()
@click.pass_context
def main(ctx):
    click.secho("CPU Benchmark", bold=True)
    results = []
    with click.progressbar(range(ctx.obj['count'])) as bar:
        for number in bar:
            response = requests.get(
                url=f'{ctx.obj["hostname"]}/api/cpu.php'
            )
            response.raise_for_status()
            results.append(
                CPUBenchmarkResult(
                    timestamp=time.time(),
                    number=number,
                    data=response.json()
                )
            )
            time.sleep(ctx.obj['sleep'])

    math_timings = [
        result.data['math']['timeTaken'] for result in results
    ]
    string_timings = [
        result.data['string']['timeTaken'] for result in results
    ]
    loops_timings = [
        result.data['loops']['timeTaken'] for result in results
    ]
    if_else_timings = [
        result.data['ifElse']['timeTaken'] for result in results
    ]
    result = {
        'results': results,
        'timings': {
            'math': {
                'min': min(math_timings),
                'max': max(math_timings),
                'mean': mean(math_timings),
                'total': sum(math_timings),
            },
            'string': {
                'min': min(string_timings),
                'max': max(string_timings),
                'mean': mean(string_timings),
                'total': sum(string_timings),
            },
            'loops': {
                'min': min(loops_timings),
                'max': max(loops_timings),
                'mean': mean(loops_timings),
                'total': sum(loops_timings),
            },
            'if_else': {
                'min': min(if_else_timings),
                'max': max(if_else_timings),
                'mean': mean(if_else_timings),
                'total': sum(if_else_timings),
            },
        }
    }
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
    click.echo(table.table)

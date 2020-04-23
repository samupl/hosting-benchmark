import time

import click
import requests

from hosting_benchmark.inc.taxonomies import BenchmarkResult
from hosting_benchmark.inc.tools import (
    calculate_timing_stats, get_timings,
    render_table
)


@click.command(help='Run the CPU benchmark')
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
                BenchmarkResult(
                    timestamp=time.time(),
                    number=number,
                    data=response.json()
                )
            )
            time.sleep(ctx.obj['sleep'])

    math_timings = get_timings(results, 'math')
    string_timings = get_timings(results, 'string')
    loops_timings = get_timings(results, 'loops')
    if_else_timings = get_timings(results, 'ifElse')
    result = {
        'results': results,
        'timings': {
            'math': calculate_timing_stats(math_timings),
            'string': calculate_timing_stats(string_timings),
            'loops': calculate_timing_stats(loops_timings),
            'if_else': calculate_timing_stats(if_else_timings),
        }
    }
    table = render_table(result)
    click.echo(table)

import time

import click
import requests

from hosting_benchmark.inc.taxonomies import BenchmarkResult
from hosting_benchmark.inc.tools import (
    calculate_timing_stats, get_timings, render_table
)


@click.command(help='Run the I/O benchmark')
@click.pass_context
def main(ctx):
    click.secho("I/O Benchmark", bold=True)
    results = []
    with click.progressbar(range(ctx.obj['count'])) as bar:
        for number in bar:
            response = requests.get(
                url=f'{ctx.obj["hostname"]}/api/io.php'
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

    create_and_remove_empty_timings = get_timings(
        results, 'createAndRemoveEmpty')
    small_write_timings = get_timings(results, 'smallWrite')
    big_write_timings = get_timings(results, 'bigWrite')
    random_write_timings = get_timings(results, 'randomWrite')

    result = {
        'results': results,
        'timings': {
            'create_and_remove_empty': calculate_timing_stats(
                create_and_remove_empty_timings),
            'small_write': calculate_timing_stats(small_write_timings),
            'big_write': calculate_timing_stats(big_write_timings),
            'random_write': calculate_timing_stats(random_write_timings),
        }
    }
    table = render_table(result)
    click.echo(table)

import time
from statistics import mean

import click
import requests
from terminaltables import SingleTable

from inc.formatters import format_timing
from inc.taxonomies import BenchmarkResult
from inc.tools import calculate_timing_stats, get_timings, render_table


@click.command()
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

    result = {
        'results': results,
        'timings': {
            'create_and_remove_empty': calculate_timing_stats(
                create_and_remove_empty_timings),
            'small_write': calculate_timing_stats(small_write_timings),
        }
    }
    table = render_table(result)
    click.echo(table)

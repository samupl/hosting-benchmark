import time

import click
import requests

from hosting_benchmark.inc.taxonomies import BenchmarkResult
from hosting_benchmark.inc.tools import (
    calculate_timing_stats, get_timings, render_table
)


@click.command(help='Run the MySQL benchmark')
@click.pass_context
def main(ctx):
    click.secho("MySQL Benchmark", bold=True)
    results = []
    with click.progressbar(range(ctx.obj['count'])) as bar:
        for number in bar:
            response = requests.get(
                url=f'{ctx.obj["hostname"]}/api/mysql.php'
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

    insert_timings = get_timings(results, 'insert')
    insert_single_transaction_timings = get_timings(
        results, 'insertSingleTransaction')
    result = {
        'results': results,
        'timings': {
            'insert': calculate_timing_stats(insert_timings),
            'insert_single_transaction': calculate_timing_stats(
                insert_single_transaction_timings),
        }
    }
    table = render_table(result)
    click.echo(table)

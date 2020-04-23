import datetime
from urllib.parse import urlparse

import click

from commands.cpu import main as cpu_benchmark


@click.group()
@click.option('--hostname', help='Hostname used to run the benchmark')
@click.option(
    '--dump',
    default=False,
    help='Dump the benchmark results',
    is_flag=True,
)
@click.option(
    '--count',
    default=25,
    help='Number of benchmark executions',
)
@click.option(
    '--sleep',
    default=10.0,
    help='Time (in seconds) to wait between executions',
)
@click.pass_context
def cli(ctx, hostname, dump, count, sleep):
    ctx.ensure_object(dict)

    # Remove trailing slash from URL
    if hostname.endswith('/'):
        hostname = hostname[:-1]

    ctx.obj['hostname'] = hostname
    ctx.obj['dump'] = dump
    ctx.obj['count'] = count
    ctx.obj['sleep'] = sleep

    if dump:
        now = datetime.datetime.now()
        now_fmt = now.strftime('%Y-%m-%d--%H-%M-%S')
        hostname_fmt = urlparse(hostname).netloc
        ctx.obj['dump_dir'] = f'results/benchmark_{hostname_fmt}_{now_fmt}'

    click.echo(f'Running benchmark for host: {ctx.obj["hostname"]}\n')


cli.add_command(cpu_benchmark, name='cpu')


if __name__ == '__main__':
    cli(obj={})

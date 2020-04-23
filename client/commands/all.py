import click

from commands.cpu import main as cpu_benchmark
from commands.io import main as io_benchmark


@click.command()
@click.pass_context
def main(ctx):
    click.secho("Full Benchmark Suite", bold=True)
    ctx.forward(cpu_benchmark)
    ctx.forward(io_benchmark)

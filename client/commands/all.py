import click

from commands.cpu import main as cpu_benchmark
from commands.io import main as io_benchmark
from commands.mysql import main as mysql_benchmark
from commands.info import main as info_command


@click.command()
@click.pass_context
def main(ctx):
    ctx.forward(info_command)

    click.secho("Full Benchmark Suite", bold=True)
    ctx.forward(cpu_benchmark)
    ctx.forward(io_benchmark)
    ctx.forward(mysql_benchmark)

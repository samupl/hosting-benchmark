import click

from hosting_benchmark.commands.cpu import main as cpu_benchmark
from hosting_benchmark.commands.io import main as io_benchmark
from hosting_benchmark.commands.mysql import main as mysql_benchmark
from hosting_benchmark.commands.info import main as info_command


@click.command(help='Run all benchmark tests')
@click.pass_context
def main(ctx):
    ctx.forward(info_command)

    click.secho("Full Benchmark Suite", bold=True)
    ctx.forward(cpu_benchmark)
    ctx.forward(io_benchmark)
    ctx.forward(mysql_benchmark)

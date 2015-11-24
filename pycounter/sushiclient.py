"""command line client to fetch statistics via SUSHI"""
from __future__ import print_function

import click


@click.command()
@click.argument('url')
@click.option('--report', '-r', default='JR1',
              help='report name (default JR1)')
@click.option('--release', '-c', default=4,
              help='COUNTER release (default 4)')
@click.option('--start_date', '-s',
              help='Start Date (default first day of last month)')
@click.option('--end_date', '-e',
              help='Start Date (default last day of last month)')
def main(url, report, release):
    click.echo("pycounter SUSHI client for URL %s (%s R%s)"
               % (url, report, release))


if __name__ == "__main__":
    main()

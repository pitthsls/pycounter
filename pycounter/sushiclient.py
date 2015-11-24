"""command line client to fetch statistics via SUSHI"""
from __future__ import print_function

from pycounter import sushi
from pycounter.helpers import convert_date_run

import click


@click.command()
@click.argument('url')
@click.option('--report', '-r', default='JR1',
              help='report name (default JR1)')
@click.option('--release', '-c', default=4,
              help='COUNTER release (default 4)')
@click.option('--start_date', '-s',
              help='Start Date YYYY-MM-DD (default first day of last month)')
@click.option('--end_date', '-e',
              help='End Date YYYY-MM-DD (default last day of last month OR '
                   'last day of start month')
@click.option('--requestor_id', '-i',
              help='Requestor ID')
@click.option('--customer_reference', '-c',
              help='Customer reference')
@click.option('--format', '-f', 'format_', default='tsv',
              help='Output format (default tsv)',
              type=click.Choice(['tsv']))
@click.option('--output_file', '-o', default='report.tsv',
              help='Output file to write (will be overwritten)',
              type=click.Path(writable=True))
def main(url, report, release, start_date, end_date, requestor_id,
         customer_reference, format_, output_file):
    # FIXME: doesn't actually default dates yet...
    click.echo("pycounter SUSHI client for URL %s (%s R%s)"
               % (url, report, release))
    report = sushi.get_report(wsdl_url=url,
                              report=report,
                              release=release,
                              requestor_id=requestor_id,
                              customer_reference=customer_reference,
                              start_date=convert_date_run(start_date),
                              end_date=convert_date_run(end_date))
    report.write_tsv(output_file)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter

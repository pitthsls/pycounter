"""command line client to fetch statistics via SUSHI."""
from __future__ import absolute_import
from __future__ import print_function

import datetime
import logging
import sys

import click

from pycounter import sushi
from pycounter.helpers import convert_date_run, last_day, prev_month

logging.basicConfig()


@click.command()
@click.argument("url")
@click.option("--report", "-r", default="JR1", help="report name (default JR1)")
@click.option("--release", "-l", default=4, help="COUNTER release (default 4)")
@click.option(
    "--start_date", "-s", help="Start Date YYYY-MM-DD (default first day of last month)"
)
@click.option(
    "--end_date",
    "-e",
    help="End Date YYYY-MM-DD (default last day of last month OR "
    "last day of start month",
)
@click.option("--requestor_id", "-i", help="Requestor ID")
@click.option("--requestor_email", help="Email address of requestor")
@click.option("--requestor_name", help="Internationally recognized organization name")
@click.option("--customer_reference", "-c", help="Customer reference")
@click.option("--customer_name", help="Internationally recognized organization name")
@click.option(
    "--format",
    "-f",
    "format_",
    default="tsv",
    help="Output format (default tsv)",
    type=click.Choice(["tsv"]),
)
@click.option(
    "--output_file",
    "-o",
    default="report.%s",
    help="Output file to write (will be overwritten)",
    type=click.Path(writable=True),
)
@click.option("--dump", "-d", is_flag=True)
@click.option("--no_ssl_verify", is_flag=True, help="Skip SSL verification")
@click.option(
    "--no-delay",
    is_flag=True,
    help="Do not delay before rerequesting a queued report. "
    "Probably don't do this to a real server.",
)
def main(
    url,
    report,
    release,
    start_date,
    end_date,
    requestor_id,
    requestor_email,
    requestor_name,
    customer_name,
    customer_reference,
    format_,
    output_file,
    dump,
    no_ssl_verify,
    no_delay,
):
    """Main function for the SUSHI client."""
    # pylint: disable=too-many-locals
    click.echo("pycounter SUSHI client for URL %s (%s R%s)" % (url, report, release))
    if end_date is not None and start_date is None:
        click.echo("Cannot specify --end_date without --start_date", err=True)
        sys.exit(1)
    if start_date is None:
        converted_start_date = prev_month(datetime.datetime.now())
    else:
        converted_start_date = convert_date_run(start_date)
    if end_date is None:
        converted_end_date = last_day(converted_start_date)
    else:
        converted_end_date = convert_date_run(end_date)
    report = sushi.get_report(
        wsdl_url=url,
        report=report,
        release=release,
        requestor_id=requestor_id,
        requestor_name=requestor_name,
        requestor_email=requestor_email,
        customer_reference=customer_reference,
        customer_name=customer_name,
        start_date=converted_start_date,
        end_date=converted_end_date,
        sushi_dump=dump,
        no_delay=no_delay,
        verify=not no_ssl_verify,
    )
    if "%s" in output_file:
        output_file = output_file % format_
    report.write_to_file(output_file, format_)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter

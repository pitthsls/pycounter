"""Helper functions used by pycounter."""
import calendar
import datetime
import re

import pendulum
import six


def convert_covered(datestring):
    """
    Convert coverage period string to datetimes.

    :param datestring: the string to convert to a date. Format as
        'YYYY-MM-DD to YYYY-MM-DD'

    :return: tuple of datetime.date instances

    (Will also accept MM/DD/YYYY format, ISO 8601 timestamps, or existing
    datetime objects; these shouldn't be in COUNTER reports, but they
    do show up in real world data...)

    Also accepts strings of the form 'Begin_Date=2019-01-01; End_Date=2019-12-31'
    for better compatibility with some (broken) COUNTER 5 implementations.
    """
    try:
        start_string, end_string = datestring.split(" to ")
    except ValueError:
        start_string, end_string = tuple(re.findall(r"\d{4}-\d{2}-\d{2}", datestring))

    start_date = convert_date_run(start_string)
    end_date = convert_date_run(end_string)

    return start_date, end_date


def convert_date_run(datestring):
    """
    Convert a date of the format 'YYYY-MM-DD' to a datetime.date object.

    (Will also accept MM/DD/YYYY format, ISO 8601 timestamps, or existing
    datetime objects; these shouldn't be in COUNTER reports, but they
    do show up in real world data...)

    :param datestring: the string to convert to a date.

    :return: datetime.date object

    """
    if isinstance(datestring, datetime.date):
        return datestring

    return pendulum.parse(datestring, strict=False).date()


def convert_date_column(datestring):
    """
    Convert human-readable month to date of first day of month.

    :param datestring: the string to convert to a date. Format like "Jan-2014".

    :return: datetime.date
    """
    return datetime.datetime.strptime(datestring.strip(), "%b-%Y").date()


def is_first_last(period):
    """

    Args:
        period: a tuple of datetime.date objects

    Returns: bool, whether the period starts on the 1st of a month and ends on
        the last of a month

    """
    if period == (None, None):
        return True
    return period[0].day == 1 and period[1].day == last_day(period[1]).day


def last_day(orig_date):
    """
    Find last day of a month from any day in the month.

    :param orig_date: the date within the month for which we want the
        last day as datetime.date

    :return: datetime.date of last day of the month

    """
    day_number = calendar.monthrange(orig_date.year, orig_date.month)[1]
    return datetime.date(orig_date.year, orig_date.month, day_number)


def next_month(dateobj):
    """Find the first day of the next month after the given date.

    :param dateobj: the date within the month for which we want the
        next month's first day as datetime.date

    :return: datetime.date of the first day of the next month

    """
    year_delta, old_month = divmod(dateobj.month, 12)
    return datetime.date(dateobj.year + year_delta, old_month + 1, 1)


def prev_month(dateobj):
    """Find the first day of the previous month before the given date.

    :param dateobj: the date within the month for which we want the
        previous month's first day as datetime.date.

    :return: datetime.date of first day of the previous month.

    """
    year_delta, old_month = divmod(dateobj.month - 2, 12)
    return datetime.date(dateobj.year + year_delta, old_month + 1, 1)


def format_stat(stat):
    """Turn numbers possibly with embedded commas into integers.

    Also accepts existing ints, which may be pre-converted from Excel.

    :param stat: numeric value, possibly with commas

    :return: int
    """
    if isinstance(stat, six.integer_types):
        return stat

    stat = stat.replace(",", "")
    stat = stat.lstrip("=")
    try:
        return int(stat)
    except ValueError:
        return 0


def guess_type_from_content(file_obj):
    """Guess type of a spreadsheet-like file.

    Defaults to assuming it's CSV, if it doesn't appear to be XLSX or TSV.

    :param file_obj: file-like object of which to determine type.

    :return: string, one of "xlsx", "tsv", "csv"
    """
    first_bytes = file_obj.read(2)
    if first_bytes == b"PK":
        filetype = "xlsx"
    else:
        content = file_obj.read()
        if b"\t" in content:
            filetype = "tsv"
        else:
            filetype = "csv"
    return filetype

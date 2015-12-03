"""Helper functions used by pycounter"""
import calendar
import datetime


def convert_covered(datestring):
    """
    Convert a string of the format 'YYYY-MM-DD to YYYY-MM-DD' to a
    tuple of datetime.date instances.

    :param datestring: the string to convert to a date.

    """
    start_string, end_string = datestring.split(" to ")
    start_date = datetime.datetime.strptime(start_string, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_string, "%Y-%m-%d").date()

    return start_date, end_date


def convert_date_run(datestring):
    """
    Convert a date of the format 'YYYY-MM-DD' to a datetime.date object

    :param datestring: the string to convert to a date.

    """
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()


def convert_date_column(datestring):
    """
    Convert a month expressed as, e.g., 'Jan-2014' to a datetime.date
    object representing the first day of that month/

    :param datestring: the string to convert to a date.

    """
    return datetime.datetime.strptime(datestring.strip(), "%b-%Y").date()


def last_day(orig_date):
    """
    Return a datetime.date object representing the last day of a
    calendar month, given a datetime.date for any day in that month

    :param orig_date: the date within the month for which we want the
        last day.

    """
    daynum = calendar.monthrange(orig_date.year, orig_date.month)[1]
    return datetime.date(orig_date.year, orig_date.month, daynum)


def next_month(dateobj):
    """Return a datetime.date for the first day of the next month
    after the given date

    :param dateobj: the date within the month for which we want the
        next month's first day.

    """
    year_delta, old_month = divmod(dateobj.month, 12)
    return datetime.date(dateobj.year + year_delta, old_month + 1, 1)


def prev_month(dateobj):
    """Return a datetime.date for the first day of the previous month
    before the given date

    :param dateobj: the date within the month for which we want the
        previous month's first day.

    """
    year_delta, old_month = divmod(dateobj.month - 2, 12)
    return datetime.date(dateobj.year + year_delta, old_month + 1, 1)


def format_stat(stat):
    """Turn string numbers that might have an embedded comma into
    integers

    :param stat: numeric value, possibly with commas, to turn into int
    """
    stat = stat.replace(',', '')
    try:
        return int(stat)
    except ValueError:
        return None


def guess_type_from_content(file_obj):
    """Given a filelike object, look for signature of various file types and
    return which one it is
    """
    first_bytes = file_obj.read(2)
    if first_bytes == b"PK":
        filetype = 'xlsx'
    else:
        content = file_obj.read()
        if b'\t' in content:
            filetype = 'tsv'
        else:
            filetype = 'csv'
    return filetype

"""COUNTER journal and book reports and associated functions"""

from __future__ import absolute_import

import logging
import re
import warnings
import datetime

import pyisbn
import six

from pycounter.exceptions import UnknownReportTypeError
from pycounter import csvhelper
from pycounter.helpers import convert_covered, convert_date_run, \
    convert_date_column, last_day, next_month


METRICS = {u"JR1": u"FT Article Requests",
           u"JR1 GOA": u"Gold Open Access Article Requests",
           u"BR1": u"Book Title Requests",
           u"BR2": u"Book Section Requests"}


class CounterReport(object):
    """
    a COUNTER usage statistics report.

    Iterate over the report object to get its rows (each of which is a
    :class:`CounterBook <CounterBook>` or :class:`CounterJournal
    <CounterJournal>` instance.

    :param metric: metric being tracked by this report. For database
        reports (which have multiple metrics per report), this should be
        set to `None`.

    :param report_type: type of report (e.g., "JR1", "BR2")

    :param report_version: COUNTER version

    :param customer: name of customer on report

    :param institutional_identifier: unique ID assigned by vendor for
        customer

    :param period: tuple of datetime.date objects corresponding to the
        beginning and end of the covered range

    :param date_run: date the COUNTER report was generated

    """

    def __init__(self, report_type=None, report_version=4, metric=None,
                 customer=None, institutional_identifier=None,
                 period=(None, None), date_run=None):
        self.pubs = []
        self.report_type = report_type
        self.report_version = report_version
        self.metric = metric
        self.customer = customer
        self.institutional_identifier = institutional_identifier
        self.period = period
        if date_run is None:
            self.date_run = datetime.date.today()
        else:
            self.date_run = date_run

    def __str__(self):
        return (
            "CounterReport %s version %s for date range %s to %s" %
            (self.report_type,
             self.report_version,
             self.period[0], self.period[1])
        )

    def __iter__(self):
        return iter(self.pubs)


class CounterEresource(six.Iterator):
    """
    base class for COUNTER statistics lines

    Iterating returns (first_day_of_month, metric, usage) tuples.

    :param line: COUNTER 3 line of data to parse

    :param period: two-tuple of datetime.date objects corresponding
        to the beginning and end dates of the covered range

    :param metric: metric tracked by this report. Should be a value
        from pycounter.report.METRICS dict.

    :param month_data: a list containing usage data for this
        resource, as (datetime.date, usage) tuples

    :param title: title of the resource

    :param publisher: name of the resource's publisher

    :param platform: name of the platform providing the resource

    """

    def __init__(self, line=None, period=None, metric=None, month_data=None,
                 title="", platform="", publisher=""):
        self.period = period
        if metric not in METRICS.values():
            warnings.warn("metric %s not known" % metric)
        self.metric = metric
        self._monthdata = []
        self._full_data = []
        if month_data is not None:
            for item in month_data:
                self._full_data.append(item)
        if line is not None:
            self.title = line[0]
            self.publisher = line[1]
            self.platform = line[2]
            self._monthdata = [format_stat(x) for x in line[5:]]
            while len(self._monthdata) < 12:
                self._monthdata.append(None)
            logging.debug("monthdata: %s", self._monthdata)

        if title:
            self.title = title
        if platform:
            self.platform = platform
        if publisher:
            self.publisher = publisher

    def __iter__(self):
        if self._full_data:
            for item in self._full_data:
                yield (item[0], self.metric, item[1])
        else:
            currmonth = self.period[0]
            mondat = iter(self._monthdata)
            while currmonth < self.period[1]:
                currusage = next(mondat)
                yield (currmonth, self.metric, currusage)
                currmonth = next_month(currmonth)


class CounterJournal(CounterEresource):
    """
    statistics for a single electronic journal.

    :param line: a list containing the usage data for this line, in
        COUNTER 3 layout. (This is an ugly hack that should be fixed
        very soon)

    :param period: two-tuple of datetime.date objects corresponding
        to the beginning and end dates of the covered range

    :param metric: the metric tracked by this statistics line.
        (Should probably always be "FT Article Requests" for
        CounterJournal objects, as long as only JR1 is supported.)

    :param issn: eJournal's print ISSN

    :param eissn: eJournal's eISSN

    :param month_data: a list containing usage data for this
        journal, as (datetime.date, usage) tuples

    :param title: title of the resource

    :param publisher: name of the resource's publisher

    :param platform: name of the platform providing the resource

    """

    def __init__(self, line=None, period=None, metric=METRICS[u"JR1"],
                 issn=None, eissn=None, month_data=None,
                 title="", platform="", publisher=""):
        super(CounterJournal, self).__init__(line, period, metric, month_data,
                                             title, platform, publisher)
        if line is not None:
            self.issn = line[3].strip()
            self.eissn = line[4].strip()
            self.isbn = None

        if issn is not None:
            self.issn = issn

        if eissn is not None:
            self.eissn = eissn

    def __str__(self):
        return """<CounterJournal %s, publisher %s,
        platform %s>""" % (self.title, self.publisher, self.platform)


class CounterBook(CounterEresource):
    """
    statistics for a single electronic book.

    :param line: a list containing the usage data for this line, in
        COUNTER 3 layout. (This is an ugly hack that should be fixed
        very soon)

    :ivar isbn: eBook's ISBN

    :ivar issn: eBook's ISSN (if any)

    :param month_data: a list containing usage data for this
        book, as (datetime.date, usage) tuples

    :param title: title of the resource

    :param publisher: name of the resource's publisher

    :param platform: name of the platform providing the resource

    """

    def __init__(self, line=None, period=None, metric=None, month_data=None,
                 title="", platform="", publisher="", isbn=None, issn=None):
        super(CounterBook, self).__init__(line, period, metric, month_data,
                                          title, platform, publisher)
        self.eissn = None
        if line is not None:
            self.isbn = line[3].strip().replace('-', '')
            if len(self.isbn) == 10:
                self.isbn = pyisbn.convert(self.isbn)
            self.issn = line[4].strip()

        if isbn is not None:
            self.isbn = isbn

        if issn is not None:
            self.issn = issn

    def __str__(self):
        return """<CounterBook %s (ISBN: %s), publisher %s,
        platform %s>""" % (self.title, self.isbn, self.publisher,
                           self.platform)


def format_stat(stat):
    """Turn string numbers that might have an embedded comma into
    integers
    """
    stat = stat.replace(',', '')
    try:
        return int(stat)
    except ValueError:
        return None


def parse(filename):
    """Parse a COUNTER file, first attempting to determine type

    Returns a :class:`CounterReport <CounterReport>` object.

    :param filename: path to COUNTER report to load and parse.

    """
    if filename.endswith('.tsv'):
        # Horrible filename-based hack; in future examine contents of file here
        return parse_separated(filename, '\t')
    if filename.endswith('.xlsx'):
        return parse_xlsx(filename)
    # fallback to old assume-csv behavior
    return parse_separated(filename, ',')


def parse_xlsx(filename):
    """Parse a COUNTER file in Excel format.

    Invoked automatically by ``parse``.

    :param filename: path to XLSX-format COUNTER report file.

    """
    from openpyxl import load_workbook

    workbook = load_workbook(filename=filename)
    worksheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])
    row_it = worksheet.iter_rows()
    split_row_list = ([cell.value if cell.value is not None else ""
                       for cell in row] for row in row_it)

    return parse_generic(split_row_list)


def parse_separated(filename, delimiter):
    """Open COUNTER CSV/TSV report with given filename and delimiter
    and parse into a CounterReport object

    Invoked automatically by :py:func:`parse`.

    :param filename: path to delimited COUNTER report file.

    :param delimiter: character (such as ',' or '\\\\t') used as the
        delimiter for this file

    """
    with csvhelper.UnicodeReader(filename,
                                 delimiter=delimiter) as report_reader:
        return parse_generic(report_reader)


def parse_generic(report_reader):
    """Takes an iterator of COUNTER report rows and
    returns a CounterReport object

    :param report_reader: a iterable object that yields lists COUNTER
        data formatted as tabular lists

    """
    report = CounterReport()

    line1 = six.next(report_reader)

    rt_match = re.match(
        r'.*(Journal|Book|Database) Report (\d(?: GOA)?) ?\(R(\d)\)',
        line1[0])
    if rt_match:
        report.report_type = (rt_match.group(1)[0].capitalize() + 'R' +
                              rt_match.group(2))
        report.report_version = int(rt_match.group(3))

    # noinspection PyTypeChecker
    report.metric = METRICS.get(report.report_type)

    report.customer = six.next(report_reader)[0]

    if report.report_version == 4:
        inst_id_line = six.next(report_reader)
        if inst_id_line:
            report.institutional_identifier = inst_id_line[0]

        six.next(report_reader)

        covered_line = six.next(report_reader)
        report.period = convert_covered(covered_line[0])

    six.next(report_reader)

    date_run_line = six.next(report_reader)
    report.date_run = convert_date_run(date_run_line[0])

    header = six.next(report_reader)
    first_date_col = 10 if report.report_version == 4 else 5
    if report.report_type in ('BR1', 'BR2') and report.report_version == 4:
        first_date_col = 8

    year = int(header[first_date_col].split('-')[1])
    if year < 100:
        year += 2000

    report.year = year

    if report.report_version == 4:
        countable_header = header[0:8]
        for col in header[8:]:
            if col:
                countable_header.append(col)
        last_col = len(countable_header)
    else:
        last_col = 0
        for val in header:
            if 'YTD' in val:
                break
            last_col += 1

        start_date = datetime.date(year, 1, 1)
        end_date = last_day(convert_date_column(header[last_col - 1]))
        report.period = (start_date, end_date)

    six.next(report_reader)
    for line in report_reader:
        if not line:
            continue
        if report.report_version == 4:
            if report.report_type.startswith('JR1'):
                line = line[0:3] + line[5:7] + line[10:last_col]
            elif report.report_type in ('BR1', 'BR2'):
                line = line[0:3] + line[5:7] + line[8:last_col]
        else:
            line = line[0:last_col]
        logging.debug(line)
        if report.report_type:
            if report.report_type.startswith('JR'):
                report.pubs.append(CounterJournal(line,
                                                  report.period,
                                                  report.metric))
            elif report.report_type.startswith('BR'):
                report.pubs.append(CounterBook(line,
                                               report.period,
                                               report.metric))
            else:
                raise UnknownReportTypeError(report.report_type)

    return report

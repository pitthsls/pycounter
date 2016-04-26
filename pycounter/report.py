"""COUNTER journal and book reports and associated functions"""

from __future__ import absolute_import

import collections
import datetime
import logging
import re

import arrow
import six

from pycounter import csvhelper
from pycounter.constants import CODES, HEADER_FIELDS, METRICS
from pycounter.constants import REPORT_DESCRIPTIONS, TOTAL_TEXT
from pycounter.exceptions import PycounterException, UnknownReportTypeError
from pycounter.helpers import convert_covered, convert_date_column, \
    convert_date_run, format_stat, guess_type_from_content, last_day, \
    next_month


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

    :param section_type: predominant section type used for this report.
        (applies to report BR2; should probably be None for any other report
        type)

    """

    def __init__(self, report_type=None, report_version=4, metric=None,
                 customer=None, institutional_identifier=None,
                 period=(None, None), date_run=None,
                 section_type=None):
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
        self.year = None
        self.section_type = section_type

    def __repr__(self):
        return (
            "<CounterReport %s version %s for date range %s to %s>" %
            (self.report_type,
             self.report_version,
             self.period[0], self.period[1])
        )

    def __iter__(self):
        return iter(self.pubs)

    def write_to_file(self, path, format_):
        """
        Output report to a file

        :param path: location to write file
        :param format_: file format. Currently supports 'tsv'
        :return:
        """
        if format_ == 'tsv':
            self.write_tsv(path)
        else:
            raise PycounterException("unknown file type %s" % format_)

    def write_tsv(self, path):
        """
        Output report to a COUNTER 4 TSV file.

        :param path: location to write file
        """
        lines = self.as_generic()
        with csvhelper.UnicodeWriter(path, delimiter='\t') as writer:
            writer.writerows(lines)

    def as_generic(self):
        """
        Output report as list of lists, containing cells that would appear
        in COUNTER report (suitable for writing as CSV, TSV, etc.)
        """
        output_lines = []
        rep_type = ""
        for name, code in CODES.items():
            if code == self.report_type[0:2]:
                rep_type = name

        report_name = ("%s Report %s (R%s)" %
                       (rep_type, self.report_type[-1], self.report_version))
        output_lines.append([report_name,
                             REPORT_DESCRIPTIONS[self.report_type]])
        if self.report_type == 'BR2':
            output_lines.append([self.customer, u'Section Type:'])
            output_lines.append([self.institutional_identifier,
                                 self.section_type])
        else:
            output_lines.append([self.customer])
            output_lines.append([self.institutional_identifier])
        output_lines.append([u'Period covered by Report:'])
        period = "%s to %s" % (
            self.period[0].strftime('%Y-%m-%d'),
            self.period[1].strftime('%Y-%m-%d')
        )
        output_lines.append([period])
        output_lines.append([u'Date run:'])
        output_lines.append([self.date_run.strftime('%Y-%m-%d')])
        output_lines.append(self._table_header())
        if self.report_type in ('JR1', 'BR1', 'BR2', 'DB2'):
            output_lines.extend(self._totals_lines())
        elif self.report_type.startswith('DB'):
            self._ensure_required_metrics()
            try:
                self.pubs.sort(
                    key=lambda x: METRICS[self.report_type].index(x.metric))
            except ValueError:
                pass

        for pub in sorted(self.pubs, key=lambda x: x.title):
            output_lines.append(pub.as_generic())

        return output_lines

    def _totals_lines(self):
        """
        Generate Totals lines for COUNTER report, as list of lists of cells
        """
        total_lines = []
        metrics = set(resource.metric for resource in self.pubs)

        for metric in sorted(metrics):
            total_lines.append(self._totals_line(metric))

        return total_lines

    def _totals_line(self, metric):
        total_cells = [
            TOTAL_TEXT[self.report_type],
        ]
        publishers = set(resource.publisher for resource in self.pubs)
        if len(publishers) == 1:
            total_cells.append(publishers.pop())
        else:
            total_cells.append(u'')
        platforms = set(resource.platform for resource in self.pubs)
        if len(platforms) == 1:
            total_cells.append(platforms.pop())
        else:
            total_cells.append(u'')
        if self.report_type in ('JR1', 'BR1', 'BR2'):
            total_cells.extend([u''] * 4)
        elif self.report_type == 'DB2':
            total_cells.append(metric)
        total_usage = 0
        pdf_usage = 0
        html_usage = 0

        number_of_months = len(
            arrow.Arrow.range('month',
                              arrow.Arrow.fromdate(self.period[0]),
                              arrow.Arrow.fromdate(self.period[1])))
        month_data = [0] * number_of_months
        for pub in self.pubs:
            if pub.metric != metric:
                continue
            if self.report_type == 'JR1':
                pdf_usage += pub.pdf_total
                html_usage += pub.html_total
            for month, data in enumerate(pub):
                total_usage += data[2]
                month_data[month] += data[2]
        total_cells.append(six.text_type(total_usage))
        if self.report_type == 'JR1':
            total_cells.append(six.text_type(html_usage))
            total_cells.append(six.text_type(pdf_usage))
        total_cells.extend(six.text_type(d) for d in month_data)
        return total_cells

    def _table_header(self):
        """
        Generate header for COUNTER table for this report, as list of cells
        """
        header_cells = list(HEADER_FIELDS[self.report_type])
        for d_obj in arrow.Arrow.range('month',
                                       arrow.Arrow.fromdate(self.period[0]),
                                       arrow.Arrow.fromdate(self.period[1])):
            header_cells.append(d_obj.strftime('%b-%Y'))
        return header_cells

    def _ensure_required_metrics(self):
        """
        Build up a dict of sets of known metrics for each database. If any
        metric is missing add a 0 use :class:`CounterDatabase<CounterDatabase>`
        Assumes platform and publisher are consistent across records
        """
        try:
            required_metrics = METRICS[self.report_type]
        except LookupError:
            raise UnknownReportTypeError(self.report_type)

        dbs = collections.defaultdict(set)
        for database in self.pubs:
            dbs[database.title].add(database.metric)

        for database, metrics in six.iteritems(dbs):
            for metric in (m for m in required_metrics if m not in metrics):
                self.pubs.append(
                    CounterDatabase(
                        title=database,
                        platform=self.pubs[0].platform,
                        publisher=self.pubs[0].publisher,
                        period=self.period,
                        metric=metric,
                        month_data=[(self.period[0], 0), ]
                    ))


class CounterEresource(six.Iterator):
    # pylint: disable=too-few-public-methods
    """
    base class for COUNTER statistics lines

    Iterating returns (first_day_of_month, metric, usage) tuples.

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

    def __init__(self, period=None, metric=None, month_data=None,
                 title="", platform="", publisher=""):
        self.period = period

        self.metric = metric
        self._full_data = []
        if month_data is not None:
            for item in month_data:
                self._full_data.append(item)

        self.title = title
        self.platform = platform
        self.publisher = publisher

    def __iter__(self):
        if self._full_data:
            for item in self._full_data:
                yield (item[0], self.metric, item[1])

    def _fill_months(self):
        """
        Check that each month in period represented and fill with zero if not
        """
        start, end = self.period[0], self.period[1]
        try:
            for d_obj in arrow.Arrow.range('month',
                                           arrow.Arrow.fromdate(start),
                                           arrow.Arrow.fromdate(end)):
                if d_obj.date() not in (x[0] for x in self._full_data):
                    self._full_data.append((d_obj.date(), 0))
        except IndexError:
            pass
        else:
            self._full_data.sort()


class CounterJournal(CounterEresource):
    """
    statistics for a single electronic journal.

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

    :param html_total: total HTML usage for this title for reporting period

    :param pdf_total: total PDF usage for this title for reporting period

    """

    def __init__(self, period=None, metric=METRICS[u"JR1"],
                 issn=None, eissn=None, month_data=None,
                 title="", platform="", publisher="", html_total=0,
                 pdf_total=0, doi="", proprietary_id=""):
        super(CounterJournal, self).__init__(period, metric, month_data,
                                             title, platform, publisher)
        self.html_total = html_total
        self.pdf_total = pdf_total
        self.doi = doi
        self.proprietary_id = proprietary_id

        self.isbn = None

        if issn is not None:
            self.issn = issn
        else:
            self.issn = ''

        if eissn is not None:
            self.eissn = eissn
        else:
            self.eissn = ''

    def __repr__(self):
        return """<CounterJournal %s, publisher %s,
        platform %s>""" % (self.title, self.publisher, self.platform)

    def as_generic(self):
        """
        return data for this line as list of COUNTER report cells
        """
        data_line = [
            self.title,
            self.publisher,
            self.platform,
            self.doi,
            self.proprietary_id,
            self.issn,
            self.eissn,
        ]
        total_usage = 0
        month_data = []
        for data in self:
            total_usage += data[2]
            month_data.append(six.text_type(data[2]))
        data_line.append(six.text_type(total_usage))
        data_line.append(six.text_type(self.html_total))
        data_line.append(six.text_type(self.pdf_total))
        data_line.extend(month_data)
        return data_line


class CounterBook(CounterEresource):
    # pylint: disable=too-few-public-methods
    """
    statistics for a single electronic book.

    :ivar isbn: eBook's ISBN

    :ivar issn: eBook's ISSN (if any)

    :param month_data: a list containing usage data for this
        book, as (datetime.date, usage) tuples

    :param title: title of the resource

    :param publisher: name of the resource's publisher

    :param platform: name of the platform providing the resource

    """

    def __init__(self, period=None, metric=None, month_data=None,
                 title="", platform="", publisher="", isbn=None, issn=None,
                 doi="", proprietary_id=""):
        super(CounterBook, self).__init__(period, metric, month_data,
                                          title, platform, publisher)
        self.eissn = None
        self.doi = doi
        self.proprietary_id = proprietary_id

        if isbn is not None:
            self.isbn = isbn
        else:
            self.isbn = u''

        if issn is not None:
            self.issn = issn
        else:
            self.issn = u''

    def __repr__(self):
        return """<CounterBook %s (ISBN: %s), publisher %s,
        platform %s>""" % (self.title, self.isbn, self.publisher,
                           self.platform)

    def as_generic(self):
        """
        return data for this line as list of COUNTER report cells
        """
        data_line = [
            self.title,
            self.publisher,
            self.platform,
            self.doi,
            self.proprietary_id,
            self.isbn,
            self.issn,
        ]
        total_usage = 0
        month_data = []
        for data in self:
            total_usage += data[2]
            month_data.append(six.text_type(data[2]))
        data_line.append(six.text_type(total_usage))
        data_line.extend(month_data)
        return data_line


class CounterDatabase(CounterEresource):
    # pylint: disable=too-few-public-methods
    """a COUNTER database report line"""

    def __init__(self, period=None, metric=None, month_data=None,
                 title="", platform="", publisher=""):
        super(CounterDatabase, self).__init__(period, metric, month_data,
                                              title, platform, publisher)
        self.isbn = None

    def as_generic(self):
        """
        return data for this line as list of COUNTER report cells
        """
        self._fill_months()

        data_line = [
            self.title,
            self.publisher,
            self.platform,
            self.metric,
        ]
        total_usage = 0
        month_data = []

        for data in self:
            total_usage += data[2]
            month_data.append(six.text_type(data[2]))

        data_line.append(six.text_type(total_usage))
        data_line.extend(month_data)

        return data_line


def parse(filename, filetype=None, encoding='utf-8',
          fallback_encoding='latin-1'):
    """Parse a COUNTER file, first attempting to determine type

    Returns a :class:`CounterReport <CounterReport>` object.

    :param filename: path to COUNTER report to load and parse.
    :param filetype: type of file provided, one of "csv", "tsv", "xlsx".
        If set to None (the default), an attempt will be made to
        detect the correct type, first from the file extension, then from
        the file's contents.
    :param encoding: encoding to use to decode the file. Defaults to 'utf-8',
        ignored for XLSX files (which specify their encoding in their XML)
    :param fallback_encoding: alternative encoding to use to try to decode
        the file if the primary encoding fails. This defaults to 'latin-1',
        which will accept any bytes (possibly producing junk results...)
        Ignored for XLSX files.

    """
    if filetype is None:
        if filename.endswith('.tsv'):
            filetype = 'tsv'
        elif filename.endswith('.xlsx'):
            filetype = 'xlsx'
        elif filename.endswith('.csv'):
            filetype = 'csv'
        else:
            with open(filename, 'rb') as file_obj:
                filetype = guess_type_from_content(file_obj)

    if filetype == 'tsv':
        return parse_separated(filename, '\t', encoding, fallback_encoding)
    elif filetype == 'xlsx':
        return parse_xlsx(filename)
    elif filetype == 'csv':
        return parse_separated(filename, ',', encoding, fallback_encoding)
    else:
        raise PycounterException("Unknown file type %s" % filetype)


def parse_xlsx(filename):
    """Parse a COUNTER file in Excel format.

    Invoked automatically by ``parse``.

    :param filename: path to XLSX-format COUNTER report file.

    """
    from openpyxl import load_workbook
    with open(filename, 'rb') as xlsx_file:
        workbook = load_workbook(xlsx_file)
        worksheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])
        row_it = worksheet.iter_rows()
        split_row_list = ([cell.value if cell.value is not None else ""
                           for cell in row] for row in row_it)

    return parse_generic(split_row_list)


def parse_separated(filename, delimiter, encoding='utf-8',
                    fallback_encoding='latin-1'):
    """Open COUNTER CSV/TSV report with given filename and delimiter
    and parse into a CounterReport object

    Invoked automatically by :py:func:`parse`.

    :param filename: path to delimited COUNTER report file.

    :param delimiter: character (such as ',' or '\\\\t') used as the
        delimiter for this file

    :param encoding: file's encoding. Default: utf-8

    :param fallback_encoding: alternative encoding to try to decode if
        default fails. Throws a warning if used.

    """
    with csvhelper.UnicodeReader(filename, delimiter=delimiter,
                                 fallback_encoding=fallback_encoding,
                                 encoding=encoding) as report_reader:
        return parse_generic(report_reader)


def parse_generic(report_reader):
    """Takes an iterator of COUNTER report rows and
    returns a CounterReport object

    :param report_reader: a iterable object that yields lists COUNTER
        data formatted as tabular lists

    """
    report = CounterReport()

    report.report_type, report.report_version = _get_type_and_version(
        six.next(report_reader)[0])

# noinspection PyTypeChecker
    report.metric = METRICS.get(report.report_type)

    report.customer = six.next(report_reader)[0]

    if report.report_version == 4:
        inst_id_line = six.next(report_reader)
        if inst_id_line:
            report.institutional_identifier = inst_id_line[0]
            if report.report_type == 'BR2':
                report.section_type = inst_id_line[1]

        six.next(report_reader)

        covered_line = six.next(report_reader)
        report.period = convert_covered(covered_line[0])

    six.next(report_reader)

    date_run_line = six.next(report_reader)
    report.date_run = convert_date_run(date_run_line[0])

    header = six.next(report_reader)

    report.year = _year_from_header(header, report)

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

        start_date = datetime.date(report.year, 1, 1)
        end_date = last_day(convert_date_column(header[last_col - 1]))
        report.period = (start_date, end_date)

    if report.report_type != 'DB1':
        six.next(report_reader)

    if report.report_type == 'DB2':
        six.next(report_reader)

    for line in report_reader:
        if not line:
            continue
        report.pubs.append(_parse_line(line, report, last_col))

    return report


def _parse_line(line, report, last_col):
    """Parse a single line from a report and return a CounterResource subclass
        instance as appropriate
    """
    issn = None
    eissn = None
    isbn = None
    html_total = 0
    pdf_total = 0
    doi = ""
    prop_id = ""

    if report.report_version == 4:
        if report.report_type.startswith('JR1'):
            old_line = line
            line = line[0:3] + line[5:7] + line[10:last_col]
            doi = old_line[3]
            prop_id = old_line[4]
            html_total = int(old_line[8])
            pdf_total = int(old_line[9])
            issn = line[3].strip()
            eissn = line[4].strip()

        elif report.report_type in ('BR1', 'BR2'):
            line = line[0:3] + line[5:7] + line[8:last_col]
            isbn = line[3].strip()
            issn = line[4].strip()

        elif report.report_type in ('DB1', 'DB2'):
            # format coincidentally works for these. This is a kludge
            # so leaving this explicit...
            pass
    else:
        if report.report_type.startswith('JR1'):
            html_total = int(line[-2])
            pdf_total = int(line[-1])
            issn = line[3].strip()
            eissn = line[4].strip()
        line = line[0:last_col]

    logging.debug(line)
    common_args = {
        'title': line[0],
        'publisher': line[1],
        'platform': line[2],
        'period': report.period
    }
    month_data = []
    curr_month = report.period[0]
    for data in line[5:]:
        month_data.append((curr_month, format_stat(data)))
        curr_month = next_month(curr_month)
    if report.report_type.startswith('JR'):
        return CounterJournal(metric=report.metric,
                              month_data=month_data,
                              doi=doi,
                              issn=issn,
                              eissn=eissn,
                              proprietary_id=prop_id,
                              html_total=html_total,
                              pdf_total=pdf_total,
                              **common_args
                              )
    elif report.report_type.startswith('BR'):
        return CounterBook(metric=report.metric,
                           month_data=month_data,
                           doi=doi,
                           issn=issn,
                           isbn=isbn,
                           proprietary_id=prop_id,
                           **common_args)
    elif report.report_type.startswith('DB'):
        return CounterDatabase(metric=line[3],
                               month_data=month_data,
                               **common_args)
    raise PycounterException("Should be unreachable")  # pragma: no cover


def _get_type_and_version(specifier):
    """Given a COUNTER report specifier, return the type and version as a tuple
    """
    report_types_clause = '|'.join(CODES)
    rt_match = re.match(
        r'.*(%s) Report (\d(?: GOA)?) ?\(R(\d)\)' % report_types_clause,
        specifier)
    if rt_match:
        report_type = (CODES[rt_match.group(1)] + rt_match.group(2))
        report_version = int(rt_match.group(3))
    else:
        raise UnknownReportTypeError("No match in line: %s" % specifier)
    if not any(report_type.startswith(x) for x in ('JR', 'BR', 'DB')):
        raise UnknownReportTypeError(report_type)

    return report_type, report_version


def _year_from_header(header, report):
    """Get the year for the report from the header

    NOTE: for multi-year reports, this will be the date of the first month,
    and probably doesn't make sense to talk of a report having a year...
    """
    first_date_col = 10 if report.report_version == 4 else 5
    if report.report_type in ('BR1', 'BR2') and report.report_version == 4:
        first_date_col = 8
    elif report.report_type == 'DB1' and report.report_version == 4:
        first_date_col = 6
    elif report.report_type == 'DB2' and report.report_version == 4:
        first_date_col = 5
    year = int(header[first_date_col].split('-')[1])
    if year < 100:
        year += 2000

    return year

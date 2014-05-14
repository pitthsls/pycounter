import csv
import logging
import re

class UnknownReportTypeError(Exception):
    pass

class CounterReport(object):
    def __init__(self):
        self.pubs = []
        self.year = None
        self.report_type = None
        self.report_version = 0

    def __str__(self):
        return "CounterReport %s version %s for %s" % (self.report_type,
                                                       self.report_version,
                                                       self.year)

    def __iter__(self):
        return iter(self.pubs)

class CounterPublication(object):
    def __init__(self, line=None):
        if line is not None:
            self.title = line[0]
            self.publisher = line[1]
            self.platform = line[2]
            self.issn = line[3].strip()
            self.eissn = line[4].strip()
            self.isbn = None
            self.monthdata = [format_stat(x) for x in line[5:]]
            while len(self.monthdata) < 12:
                self.monthdata.append(None)
            logging.debug("monthdata: %s", self.monthdata)
    def __str__(self):
        return """<CounterPublication %s, publisher %s,
        platform %s>""" % (self.title, self.publisher, self.platform)

class CounterBook(object):
    def __init__(self, line=None):
        if line is not None:
            self.title = line[0]
            self.publisher = line[1]
            self.platform = line[2]
            self.isbn = line[3].strip()
            self.issn = line[4].strip()
            self.eissn = None
            self.monthdata = [format_stat(x) for x in line[5:]]
            while len(self.monthdata) < 12:
                self.monthdata.append(None)
            logging.debug("monthdata: %s", self.monthdata)

def format_stat(stat):
    stat = stat.replace(',', '')
    try:
        return int(stat)
    except ValueError:
        return None

def parse(filename):
    """Parse a COUNTER file, first attempting to determine type"""
    if filename.endswith('.tsv'):
        # Horrible filename-based hack; in future examine contents of file here
        return parse_tsv(filename)

    # fallback to old assume-csv behavior
    return parse_csv(filename)


def parse_csv(filename):
    """Open COUNTER CSV report with given filename and parse into a
    CounterReport object"""
    with open(filename, 'rb') as datafile:
        report = CounterReport()

        report_reader = csv.reader(datafile)
        line1 = report_reader.next()
        parts = line1[0].split()

        rt_match = re.match(r'.*(Journal|Book|Database) Report (\d) ?\(R(\d)\)',
                            line1[0])
        if rt_match:
            report.report_type = (rt_match.group(1)[0].capitalize()+ 'R' +
                     rt_match.group(2))
            report.report_version = int(rt_match.group(3))

        for _ in xrange(3):
            report_reader.next()
        if report.report_version == 4:
            # COUNTER 4 has 3 more lines of introduction
            for _ in xrange(3):
                report_reader.next()
        header = report_reader.next()
        first_date_col = 10 if report.report_version == 4 else 5
        report.year = int(header[first_date_col].split('-')[1])
        if report.year < 100:
            report.year += 2000

        if report.report_version == 4:
            last_col = len(header)
        else:
            for last_col, v in enumerate(header):
                if 'YTD' in v:
                    break
        report_reader.next()
        for line in report_reader:
            if not line:
                continue
            if report.report_version == 4:
                line = line[0:3] + line[5:7] + line[10:last_col]
            else:
                line = line[0:last_col]
            logging.debug(line)
            if report.report_type:
                if report.report_type.startswith('JR'):
                    report.pubs.append(CounterPublication(line))
                elif report.report_type.startswith('BR'):
                    report.pubs.append(CounterBook(line))
                else:
                    raise UnknownReportTypeError(report.report_type)

        return report

def parse_tsv(filename):
    """Open COUNTER TSV report with given filename and parse into a
    CounterReport object"""
    with open(filename, 'rb') as datafile:
        report = CounterReport()

        report_reader = csv.reader(datafile, delimiter="\t")
        line1 = report_reader.next()
        parts = line1[0].split()

        rt_match = re.match(r'.*(Journal|Book|Database) Report (\d) ?\(R(\d)\)',
                            line1[0])
        if rt_match:
            report.report_type = (rt_match.group(1)[0].capitalize()+ 'R' +
                     rt_match.group(2))
            report.report_version = int(rt_match.group(3))

        for _ in xrange(3):
            report_reader.next()
        if report.report_version == 4:
            # COUNTER 4 has 3 more lines of introduction
            for _ in xrange(3):
                report_reader.next()
        header = report_reader.next()
        first_date_col = 10 if report.report_version == 4 else 5
        report.year = int(header[first_date_col].split('-')[1])
        if report.year < 100:
            report.year += 2000

        if report.report_version == 4:
            last_col = len(header)
        else:
            for last_col, v in enumerate(header):
                if 'YTD' in v:
                    break
        report_reader.next()
        for line in report_reader:
            if not line:
                continue
            if report.report_version == 4:
                line = line[0:3] + line[5:7] + line[10:last_col]
            else:
                line = line[0:last_col]
            logging.debug(line)
            if report.report_type:
                if report.report_type.startswith('JR'):
                    report.pubs.append(CounterPublication(line))
                elif report.report_type.startswith('BR'):
                    report.pubs.append(CounterBook(line))
                else:
                    raise UnknownReportTypeError(report.report_type)

        return report

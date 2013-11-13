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
            print(line)
            self.monthdata = [format_stat(x) for x in line[5:]]
            while len(self.monthdata) < 12:
                self.monthdata.append(None)
            logging.debug("monthdata: %s", self.monthdata)

def format_stat(stat):
    stat = stat.replace(',', '')
    if stat.isdigit():
        return int(stat)
    else:
        return None

def parse(filename):
    """Open CSV COUNTER report with given filename and parse into a
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
        header = report_reader.next()
        report.year = int(header[5].split('-')[1])
        if report.year < 100:
            report.year += 2000

        for last_row, v in enumerate(header):
            if 'YTD' in v:
                break
        report_reader.next()
        for line in report_reader:
            if not line:
                continue
            line = line[0:last_row]
            logging.debug(line)
            if report.report_type:
                if report.report_type.startswith('JR'):
                    report.pubs.append(CounterPublication(line))
                elif report.report_type.startswith('BR'):
                    report.pubs.append(CounterBook(line))
                else:
                    raise UnknownReportTypeError(report.report_type)

        return report

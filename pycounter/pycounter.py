import csv
import logging
import re

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
            self.publisher = line[1]
            self.platform = line[2]
            self.issn = line[3]
            self.eissn = line[4]
            self.monthdata = [int(x) for x in line[5:-3]]
            while len(self.monthdata) < 12:
                self.monthdata.append(None)
            logging.debug("monthdata: %s", self.monthdata)

def parse(filename):
    """Open COUNTER report with given filename and parse into a CounterReport object"""
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

        report.report_version = int(parts[3][-2])
        for _ in xrange(3):
            report_reader.next()
        header = report_reader.next()
        report.year = int(header[5].split('-')[1])
        report_reader.next()
        for line in report_reader:
            logging.debug(line)
            report.pubs.append(CounterPublication(line))

        return report

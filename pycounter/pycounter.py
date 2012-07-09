import csv
import logging

class CounterReport(object):
    def __init__(self):
        self.pubs = []
        self.year = None
        self.report_type = None
        self.report_version = 0

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
            logging.debug("monthdata: %s", self.monthdata)

def parse(filename):
    """Open COUNTER report with given filename and parse into a CounterReport object"""
    with open(filename, 'rb') as datafile:
        report = CounterReport()

        report_reader = csv.reader(datafile)
        line1 = report_reader.next()
        parts = line1[0].split()
        report.report_type = ""
        if parts[1] == "Journal":
            report.report_type += "JR"
        report.report_type += parts[3][0]
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

"""Read CSV as unicode from both python 2 and 3 transparently"""
from __future__ import absolute_import

import csv
import six


# noinspection PyUnusedLocal
class UnicodeReader(six.Iterator):
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if six.PY3:
            self.f = open(self.filename, 'rt',
                          encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'rb')
        self.reader = csv.reader(self.f, dialect=self.dialect,
                                 **self.kw)
        return self

    def __exit__(self, type_, value, traceback):
        self.f.close()

    def __next__(self):
        row = next(self.reader)
        if six.PY3:
            return row
        return [s.decode("utf-8") for s in row]

    def __iter__(self):
        return self


# noinspection PyUnusedLocal
class UnicodeWriter(object):
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if six.PY3:
            self.f = open(self.filename, 'wt',
                          encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'wb')
        self.writer = csv.writer(self.f, dialect=self.dialect,
                                 **self.kw)
        return self

    def __exit__(self, type_, value, traceback):
        self.f.close()

    def writerow(self, row):
        if not six.PY3:
            row = [s.encode(self.encoding) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

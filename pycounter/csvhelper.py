"""Read CSV as unicode from both python 2 and 3 transparently"""
from __future__ import absolute_import

import csv
import warnings

import six


# noinspection PyUnusedLocal
class UnicodeReader(six.Iterator):
    # pylint: disable=too-few-public-methods
    """CSV reader that can handle unicode"""
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", fallback_encoding="latin-1", **kwargs):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kwargs = kwargs
        self.fileobj = None
        self.reader = None
        self.fallback_encoding = fallback_encoding

    def __enter__(self):
        if six.PY3:
            self.fileobj = open(self.filename, 'rt',
                                encoding=self.encoding, newline='')
            try:
                self.fileobj.read()
            except UnicodeDecodeError:
                warnings.warn("Decoding with '%s' codec failed; falling "
                              "back to '%s'" % (self.encoding,
                                                self.fallback_encoding))
                self.fileobj = open(self.filename, 'rt',
                                    encoding=self.fallback_encoding,
                                    newline='')
                self.encoding = self.fallback_encoding
            finally:
                self.fileobj.seek(0)
        else:
            self.fileobj = open(self.filename, 'rb')
            try:
                self.fileobj.read().decode(self.encoding)
            except UnicodeDecodeError:
                warnings.warn("Decoding with '%s' codec failed; falling "
                              "back to '%s'" % (self.encoding,
                                                self.fallback_encoding))
                self.encoding = self.fallback_encoding
            finally:
                self.fileobj.seek(0)
        self.reader = csv.reader(self.fileobj, dialect=self.dialect,
                                 **self.kwargs)
        return self

    def __exit__(self, type_, value, traceback):
        self.fileobj.close()

    def __next__(self):
        row = next(self.reader)
        if six.PY3:
            return row
        return [s.decode(self.encoding) for s in row]

    def __iter__(self):
        return self


# noinspection PyUnusedLocal
class UnicodeWriter(object):
    """CSV writer that can handle unicode"""
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", lineterminator='\n', **kwargs):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.lineterminator = lineterminator
        self.kwargs = kwargs
        self.writer = None
        self.fileobj = None

    def __enter__(self):
        if six.PY3:
            self.fileobj = open(self.filename, 'wt',
                                encoding=self.encoding, newline='')
        else:
            self.fileobj = open(self.filename, 'wb')
        self.writer = csv.writer(self.fileobj, dialect=self.dialect,
                                 lineterminator=self.lineterminator,
                                 **self.kwargs)
        return self

    def __exit__(self, type_, value, traceback):
        self.fileobj.close()

    def writerow(self, row):
        """write a row to the output

        :param row: list of cells to write to the file
        """
        if not six.PY3:
            row = [(s or '').encode(self.encoding) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        """write many rows to the output

        :param rows: list of lists of cells to write
        """
        for row in rows:
            self.writerow(row)

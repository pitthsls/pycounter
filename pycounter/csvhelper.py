"""Read CSV as unicode from both python 2 and 3 transparently."""

import csv
import warnings


# noinspection PyUnusedLocal
class UnicodeReader:
    """CSV reader that can handle unicode.

    Must be used as a context manager:

    with UnicodeReader('myfile.csv') as reader:
        pass # do things with reader

    :param filename: path to file to open
    :param dialect: a csv.Dialect instance or dialect name
    :param encoding: text encoding of file
    :param fallback_encoding: encoding to fall back to if default
             encoding fails; gives warning if it's used.

    All other parameters will be passed through to csv.reader()
    """

    def __init__(
        self,
        filename,
        dialect=csv.excel,
        encoding="utf-8",
        fallback_encoding="latin-1",
        **kwargs
    ):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kwargs = kwargs
        self.fileobj = None
        self.reader = None
        self.fallback_encoding = fallback_encoding

    def __enter__(self):
        self.fileobj = open(self.filename, "rt", encoding=self.encoding, newline="")
        try:
            self.fileobj.read()
        except UnicodeDecodeError:
            warnings.warn(
                "Decoding with '%s' codec failed; falling "
                "back to '%s'" % (self.encoding, self.fallback_encoding)
            )
            self.fileobj = open(
                self.filename, "rt", encoding=self.fallback_encoding, newline=""
            )
            self.encoding = self.fallback_encoding
        finally:
            self.fileobj.seek(0)
        self.reader = csv.reader(self.fileobj, dialect=self.dialect, **self.kwargs)
        return self

    def __exit__(self, type_, value, traceback):
        self.fileobj.close()

    def __next__(self):
        return next(self.reader)

    def __iter__(self):
        return self


# noinspection PyUnusedLocal
class UnicodeWriter:
    """CSV writer that can handle unicode.

    Must be used as a context manager:

    with UnicodeWriter('myfile.csv') as writer:
        pass # do things with writer

    :param filename: path to file to open
    :param dialect: a csv.Dialect instance or dialect name
    :param encoding: text encoding of file

    All other parameters will be passed through to csv.writer()
    """

    def __init__(
        self,
        filename,
        dialect=csv.excel,
        encoding="utf-8",
        lineterminator="\n",
        **kwargs
    ):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.lineterminator = lineterminator
        self.kwargs = kwargs
        self.writer = None
        self.fileobj = None

    def __enter__(self):
        self.fileobj = open(self.filename, "wt", encoding=self.encoding, newline="")
        self.writer = csv.writer(
            self.fileobj,
            dialect=self.dialect,
            lineterminator=self.lineterminator,
            **self.kwargs
        )
        return self

    def __exit__(self, type_, value, traceback):
        self.fileobj.close()

    def writerow(self, row):
        """Write a row to the output.

        :param row: list of cells to write to the file
        """
        self.writer.writerow(row)

    def writerows(self, rows):
        """Write many rows to the output.

        :param rows: list of lists of cells to write
        """
        for row in rows:
            self.writerow(row)

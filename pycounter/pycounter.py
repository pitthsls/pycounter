# flake8: noqa
from __future__ import absolute_import
import warnings

from pycounter.report import (CounterReport, CounterPublication, CounterBook,
                              format_stat, parse, parse_xlsx, parse_csv,
                              parse_tsv)

__all__ = [CounterBook, CounterPublication, CounterReport,
           format_stat, parse, parse_xlsx, parse_csv, parse_tsv]

warnings.warn("""pycounter.pycounter is deprecated; all content
has been moved to pycounter.report.""", DeprecationWarning)

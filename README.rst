pycounter
=========

.. image:: https://travis-ci.org/pitthsls/pycounter.svg?branch=master
    :target: https://travis-ci.org/pitthsls/pycounter
    
.. image:: https://ci.appveyor.com/api/projects/status/lochuaf25fa9inru/branch/master?svg=true
    :target: https://ci.appveyor.com/project/Wooble/pycounter/branch/master

.. image:: https://coveralls.io/repos/pitthsls/pycounter/badge.svg?branch=master
    :target: https://coveralls.io/r/pitthsls/pycounter?branch=master

.. image:: https://img.shields.io/pypi/v/pycounter.svg
    :target: https://pypi.org/project/pycounter/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/pycounter/badge/?version=stable
    :target: https://readthedocs.org/projects/pycounter/?badge=stable
    :alt: Documentation Status


pycounter makes working with `COUNTER <http://www.projectcounter.org/>`_
usage statistics in Python easy, including fetching statistics with NISO
`SUSHI <http://www.niso.org/workrooms/sushi>`_.

A simple command-line client for fetching JR1 reports from SUSHI servers
and outputting them as tab-separated COUNTER 4 reports is included.

Developed by the `Health Sciences Library System <http://www.hsls.pitt.edu>`_ 
of the `University of Pittsburgh <http://www.pitt.edu>`_  to support importing
usage data into our in-house Electronic Resources Management (ERM) system.

Licensed under the MIT license. See the file LICENSE for details.

pycounter is tested on Python 2.7, 3.4, 3.5, 3.6 and pypy2 (if you're still stuck on
Python 2.6 or 3.3, please use version 0.16.1 of pycounter)

Documentation is on `Read the Docs <http://pycounter.readthedocs.io>`_.


Installing
----------
From `pypi <https://pypi.org/project/pycounter/>`_:

    pip install pycounter

From inside the source distribution:

    pip install [-e] .

(use -e if you plan to work on the source itself, so your changes are used in your installation.
Probably do all of this in a virtualenv. `The PyPA <https://packaging.python.org/tutorials/installing-packages/>`_
has a good explanation of how to get started.)

Usage
-----

Parsing COUNTER reports (currently supports COUNTER 3 and 4, in .csv, .tsv, 
or .xlsx files, reports JR1, DB1, DB2, BR1, and BR2)::

    >>> import pycounter.report
    >>> report = pycounter.report.parse("COUNTER4_2015.tsv")  # filename or path to file
    >>> print(report.metric)
    FT Article Requests
    >>> for journal in report:
    ...     print(journal.title)
    Sqornshellous Swamptalk
    Acta Mattressica
    >>> for stat in report.pubs[0]:
    ...     print(stat)
    (datetime.date(2015, 1, 1), 'FT Article Requests', 120)
    (datetime.date(2015, 2, 1), 'FT Article Requests', 42)
    (datetime.date(2015, 3, 1), 'FT Article Requests', 23)
    
Fetching SUSHI data::

    >>> import pycounter.sushi
    >>> import datetime
    >>> report = pycounter.sushi.get_report(wsdl_url='http://www.example.com/SushiService',
    ...     start_date=datetime.date(2015,1,1), end_date=datetime.date(2015,1,31),
    ...     requestor_id="myreqid", customer_reference="refnum", report="JR1",
    ...     release=4)
    >>> for journal in report:
    ...     print(journal.title)
    Sqornshellous Swamptalk
    Acta Mattressica

Output of report as TSV::

    >>> report.write_tsv("/tmp/counterreport.tsv")


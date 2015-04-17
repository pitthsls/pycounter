pycounter
=========

.. image:: https://travis-ci.org/pitthsls/pycounter.svg?branch=master
    :target: https://travis-ci.org/pitthsls/pycounter

.. image:: https://coveralls.io/repos/pitthsls/pycounter/badge.svg?branch=master
    :target: https://coveralls.io/r/pitthsls/pycounter?branch=master

.. image:: https://pypip.in/version/pycounter/badge.svg
    :target: https://pypi.python.org/pypi/pycounter/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/pycounter/badge/?version=stable
    :target: https://readthedocs.org/projects/pycounter/?badge=stable
    :alt: Documentation Status


pycounter makes working with `COUNTER <http://www.projectcounter.org/>`_
usage statistics in Python easy, including fetching statistics with NISO
`SUSHI <http://www.niso.org/workrooms/sushi>`_.

Developed by the `Health Sciences Library System <http://www.hsls.pitt.edu>`_ 
of the `University of Pittsburgh <http://www.pitt.edu>`_  to support importing
usage data into our in-house Electronic Resources Management (ERM) system.

Licensed under the MIT license. See the file LICENSE for details.

pycounter is tested on Python 2.6, 2.7, 3.3, 3.4, 3.5, and pypy2

Documentation is on `Read the Docs <http://pycounter.readthedocs.org>`_.


Installing
----------
From `pypi <http://pypi.python.org/pypi/pycounter>`_:

    pip install pycounter

From inside the source distribution:

    python setup.py install

**About dependencies:** pycounter uses
`lxml <http://lxml.de/>`_, an XML parsing library with a C extension.
It requires libxml2 and libxslt to be installed to build correctly.
It may be helpful to install lxml manually before installing pycounter,
either with the Windows binary installers,
a linux distro package, or with macports or homebrew on OS X. See the
`lxml installation docs <http://lxml.de/installation.html>`_ for more
information.
    
Usage
-----

Parsing COUNTER reports (currently supports COUNTER 3 and 4, in .csv, .tsv, 
or .xlsx files, reports JR1, BR1, and BR2)::

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
    ...     startdate=datetime.date(2015,1,1), enddate=datetime.date(2015,1,31),
    ...     requestor_id="myreqid", customer_reference="refnum", report="JR1",
    ...     release=4)
    >>> for journal in report:
    ...     print(journal.title)
    Sqornshellous Swamptalk
    Acta Mattressica


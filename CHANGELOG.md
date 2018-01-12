# Changelog

## 1.0.0

* Dropped support for python 2.6 and 3.3

## 0.16

### CounterBook

* CounterBook.isbn is now a property; it will evaluate to the generic ISBN 
given in a tabular report (or the constructor, manually), if any, or to an 
Online_ISBN or Print_ISBN given in an XML report, if they exist, in that 
order. CounterBook.online_isbn and CounterBook_print_isbn added. [Geoffrey 
Spear]

## 0.15.3

### Other

* Travis: 3.6 released; use it for pyflakes and remove -dev tag. [Geoffrey Spear]

* Travis: add 3.6-dev env. [Geoffrey Spear]

* Tox: test on py36 and py37. [Geoffrey Spear]

* Include a user-agent header in SUSHI requests; issue #46. [Geoffrey Spear]

* Move some fixtures to conftest.py to get rid of shadowing warnings; some more unittest-&gt;pytest conversions. [Geoffrey Spear]

* (not sure this file is even useful at all... but now it's useless in pytest) [Geoffrey Spear]

* Test_helpers moved to pytest. [Geoffrey Spear]

* Remove a looped assert, and convert last use of unittest in this file. [Geoffrey Spear]

* More pytest. [Geoffrey Spear]

* Bump version for unreleased dev code. [Geoffrey Spear]

* Move some tests to pure-pytest; parameterize instead of having repeated code and multiple asserts per method... [Geoffrey Spear]

* Add dump flag to sushiclient to generate XML dumps. [Geoffrey Spear]


## 0.15.1 (2016-08-31)

### Other

* New version of requests needs headers to all be strings; old version accepted int content-length. [Geoffrey Spear]

  (Bump version for bugfix)

* One more try. [Geoffrey Spear]

* Pin flake8 too. [Geoffrey Spear]

* Pin flake8-import-order version to before 2.6 support was dropped. [Geoffrey Spear]

* Flake8: missing a single whitespace broke the build. [Geoffrey Spear]

* Openpyxl get_sheet_names and get_sheet_by_name were warning about deprecation; change to use new syntax to access this information. [Geoffrey Spear]

  .gitignore some junk that pycharm creates

* Openpyxl get_sheet_names and get_sheet_by_name were warning about deprecation; change to use new syntax to access this information. [Geoffrey Spear]

* Merge pull request #44 from pitthsls/issue22. [Geoffrey Spear]

  Issue22

* Install coverage in test env (travis was warning about it not being there) [Geoffrey Spear]

* Add a pip cache on Travis. [Geoffrey Spear]

* Make tox use pytest; have travis use tox-travis. [Geoffrey Spear]

* Stop calling this an alpha since it's working well... [Geoffrey Spear]

* Style: format docstrings according to PEP 257 (verify with pydocstyle) [Geoffrey Spear]

* Some style corrections per pylint; a bit of test DRYing. [Geoffrey Spear]

* Document UnicodeReader, UnicodeWriter. [Geoffrey Spear]

* Bump version for dev; enable branch coverage measurement, switch to pytest as test runner on travis. [Geoffrey Spear]


## 0.14.0 (2016-05-18)

### Other

* Wiley seems to be finicky about capitalization of at least the ID attibrute here... following SUSHIStarters' practice and sending with capitals. [Geoffrey Spear]

* Merge pull request #38 from withnale/provide_exceptions. [Geoffrey Spear]

  Provide context when sushi exception is generated

* Provide context when sushi exception is generated. [Paul Rhodes]

* Merge pull request #40 from withnale/report_type_support. [Geoffrey Spear]

  Added definitions to JR2,JR3,BR3 counter types

* Added definitions to JR2,JR3,BR3 counter types. [Paul Rhodes]

* Merge pull request #39 from withnale/avoid_none_column_errors. [Geoffrey Spear]

  Ensure that the encode method doesn't fail if the cell value is None

* Ensure encode does not fail when cell value is None. [Paul Rhodes]

* Update RTD link for their new domain. [Geoffrey Spear]

* BR2: get section type from the report, instead of hardcoding &quot;Chapter&quot; on output... [Geoffrey Spear]

* Merge pull request #33 from chill17/dbsushicodequality. [Geoffrey Spear]

  DB Sushi Code Quality

* Removed assertIn in tests for 2.6 compatability. [Ed Hill]

* Change sushi.py to work with DB_METRIC_MAP and configured tests for new output. [Ed Hill]

* Use DB_METRIC_MAP to map metric names from SUSHI to be consistent with the API. [Ed Hill]

* Make ensure_required_metrics work with METRICS and move sort out of method. [Ed Hill]

* Removed hardcoded DB metrics from report.py. [Ed Hill]

* Moved DB1 and DB2 metrics and mapping to constants.py. [Ed Hill]

* Document write_to_file and don't redefine format() builtin accidentally... [Geoffrey Spear]

* Flake8: missing whitespace. [Geoffrey Spear]

* Bump version, eliminate pylint unused variables complaints, prepare for more export formats. [Geoffrey Spear]

* Add module docstrings to the test suite. [Geoffrey Spear]

* Merge pull request #31 from chill17/addingdbtosushi. [Geoffrey Spear]

  Add DB1 and DB2 report processing to SUSHI

* Replace set comprehension with generator expression for Py2.6. [Ed Hill]

* Fixed pyflakes formatting issues. [Ed Hill]

* Variable names more explicit and set() call removed from loop. [Ed Hill]

* Added tests and data files for DB reports through SUSHI. [Ed Hill]

  TestConvertRawDatabase tests that all information is
  correct and in the correct order for a DB report.
  Utilizes sushi_simple_db1.xml which is in part based
  on formatting from ProQuest SUSHI reports

  TestRawDatabaseWithMissingData tests that, on output,
  SUSHI data is correct and full even if zero-value fields
  were not sent. January is missing data and there are no
  records for 'record_view' in the data source. Utilizes
  sushi_db1_missing_record_view.xml which is in part based
  on formatting from EBSCO SUSHI reports.

* Add method to CounterReport to insert missing metrics. [Ed Hill]

  SUSHI protocol does not guarantee fields with zero use
  are in a report. If a field has no use for a given
  period, it might not show up in the report at all.

  If a report is a datbase report, check each database
  to ensure it has all metrics and insert them with a 0
  for the first month of the reporting period. After all
  metrics have been established, sort them so they write
  to file in the correct order (sort order will be
  maintained after the subsequent title sort)

* Add method to CounterEresource to fill empty months. [Ed Hill]

  SUSHI protocol does not require transmission of
  fields with zero use. Ensures months with no data
  are inserted with a 0, then sorted. Calls from
  CounterDatabase.as_generic to accurately write as a
  COUNTER compliant report.

* Convert SUSHI metric codes to COUNTER metric names. [Ed Hill]

  Provide a mapping from SUSHI codes to COUNTER names
  for DB reports. If parsing a pre-formatted COUNTER
  report, it will fall back to whatever is already in
  the report.

* Added support for DB reports to be collected through SUSHI. [Ed Hill]

  DB reports are different because they have multiple metrics
  on multiple lines, and SUSHI protocol provides limited
  guarantees on how they will be formatted. Catch month values
  in a dict with metrics as keys, then send each as a
  CounterDatabase object

* Fix documentation a bit. [Geoffrey Spear]

* Giving up on pypy3 ever working (they're still using python 3.2, which we don't support anyway); removing expected failures since 3.6 is working now. [Geoffrey Spear]


## 0.13.0 (2016-04-05)

### Other

* Only pin lxml version on PyPy 2. [Geoffrey Spear]

* Only pin lxml version on PyPy. [Geoffrey Spear]

* Bump version since SUSHI API changes... [Geoffrey Spear]

* Add customer name to SUSHI. [Geoffrey Spear]

* Add requestor name to SUSHI requests; make it possible to specify name and email in the client. [Geoffrey Spear]

* Enables logging output in sushiclient; use a UUID for request ID. [Geoffrey Spear]

* Add &quot;created&quot; attribute to ReportRequest. Fix #30. [Geoffrey Spear]

* Suppress logging and warning output in unit tests... These are expected and there's no point in outputting them... [Geoffrey Spear]


## 0.12.0 (2016-03-17)

### Other

* Bump version for release. [Geoffrey Spear]

* Set title and platform attributes on CounterResource even if they're blank... [Geoffrey Spear]

* Order output reports by title. Fix #28. [Geoffrey Spear]

  (Also correct missing line at EOF in last commit)

* Add a test of bad content in CSV, not just Excel (which does more magic conversion behind the scenes before it even hits our code...) [Geoffrey Spear]

* Style/refactor: rename some locals, adjust some docs, to make pycharm inspections happier... [Geoffrey Spear]

* Travis: wrong YAML syntax... [Geoffrey Spear]

* Travis: print coverage report into log (coveralls being down shouldn't make it impossible to view coverage on the web...) [Geoffrey Spear]

* Py2: checking for int objects isn't enough in py2, since these get converted as longs. Use six. [Geoffrey Spear]

* Be more accepting of Excel dates formatted as dates (instead of COUNTER-mandated date format strings), Weirdly formatted date strings, commas in data. [Geoffrey Spear]

  ( issue #15 )

* Fix typo in docstring. [Geoffrey Spear]

* Some tiny reformatting. [Geoffrey Spear]

* Update copyright dates. [Geoffrey Spear]

* Warning when fallback encoding is used... [Geoffrey Spear]

* Bump version since the API is changing with encoding stuff... [Geoffrey Spear]

* Fall back to 'latin-1' codec (or any specified encoding) when reading files. Fixes issue #26. [Geoffrey Spear]

* Py2: missed this hardcoded utf-8 instead of using self.encoding... [Geoffrey Spear]

* Allow encoding to be specified for separated files. See issue #26. [Geoffrey Spear]

* Fix typo. [Geoffrey Spear]

* Coverage: add SUSHI book with blank value for ISBN fields. [Geoffrey Spear]

* Remove mock that was added then never used. [Geoffrey Spear]

* Merge pull request #27 from chill17/publisher-fix. [Geoffrey Spear]

  Removed if condition for setting self.publisher from CounterEresource

* Removed if condition for setting self.publisher from CounterEresource class. [Ed Hill]

  ItemPublisher is listed in schema with minOccurs=&quot;0&quot;
  Not required for every field for valid Counter report
  When if condition fails and self.publisher is not set various methods
  such as CounterReport.write_tsv throw AttributeError exceptions because
  they assume self.publisher.
  Causes failure of writing and reading reports from some Counter compliant
  vendors.

* Bump version for dev... [Geoffrey Spear]

* SUSHI book report: set ISBN from Online_ISBN field. Fix #25. [Geoffrey Spear]


## 0.11.1 (2016-01-25)

### Other

* Bump version for release. [Geoffrey Spear]

* Catch and ignore AttributeError when trying to iterate over SUSHI ItemIdentifier tags; possibly none will be present. Fix #24. [Geoffrey Spear]

* Add failing test for #24 (missing ItemIdentifiers causing error) [Geoffrey Spear]


## 0.11.0 (2016-01-20)

### Other

* Unpin openpxyl version; possibly pypy bug is fixed? (Issue on bitbucket looks closed, not 100% sure fix was released) [Geoffrey Spear]

* Update README to reflect that not only JR is supported by write_tsv (all report types supported for parsing can be output now); bump version for release. [Geoffrey Spear]

* Coverage: have a new file with 2-digit years since we dropped coverage by insisting BR2 did parse-export roundtrip correctly. [Geoffrey Spear]

* Add support for BR2 output. Fix #9. [Geoffrey Spear]

* Py2.6: no set literal syntax; just use a tuple, it's not slower for such a small test. [Geoffrey Spear]

* Add support for output of DB reports (DB1, DB2); fix some style issues. [Geoffrey Spear]

* Coverage: test file with multiple publishers and platforms (should bring us to 100% coverage) [Geoffrey Spear]

* Coverage: remove ISSNs from 1 SUSHI file to cover bit that deals with missing ISSNs. [Geoffrey Spear]

* Coverage: test creation of blank CounterJournal item. [Geoffrey Spear]

* If all publications have the same publisher, include the publisher name in the totals line. fix #23. [Geoffrey Spear]

* Use correct format for Platform report, even if it's bogus... [Geoffrey Spear]

* Pull report types for regex from constant instead of hardcoding. [Geoffrey Spear]

* Test valid but unsupported report type (Platform Report) [Geoffrey Spear]

* Remove some dead code; no idea if this actually ever did anything. [Geoffrey Spear]

* (coverage): don't cover line asserting it's unreachable. [Geoffrey Spear]

  Test unknown file type raises exception.

* (coverage): check that extra blank lines at the end of a file doesn't trip up the parser. [Geoffrey Spear]

* Change some __str__ methods to __repr__ and skip checking coverage for them... [Geoffrey Spear]

* Whoops... this test passes on Windows because of case-insensitive file system; fails on Travis. [Geoffrey Spear]

* Flake8: missed newline at end of file :( [Geoffrey Spear]

* Add support for output of report BR1. [Geoffrey Spear]

* Move hardcoded header column cells to a constant. [Geoffrey Spear]

* Document missing sushiclient options; a bit more code quality stuff. [Geoffrey Spear]

* Tweak BR1 SUSHI response a bit to make it more book-like and for code coverage. [Geoffrey Spear]

* Test SUSHI for book reports (The report could... use some work. Just based it off the JR1 report, and it's probably largely invalid but the parser doesn't care) [Geoffrey Spear]

* More tests for the SUSHI client. [Geoffrey Spear]

* Python 2.6 doesn't have assertIn; skip coverage check for __name__ == &quot;__main__&quot; guard. [Geoffrey Spear]

* Add a simple test of the SUSHI client. [Geoffrey Spear]


## 0.10.1 (2015-12-04)

### Other

* Bump version for tiny test fix, and release this instead. [Geoffrey Spear]

* Python 2.6 doesn't have assertIsNone... [Geoffrey Spear]


## 0.10 (2015-12-04)

### Other

* Restore isbn attribute to CounterJournal and CounterDatabase objects; the attribute should consistently exist on CounterEresources even if it's None. Tag version for release. [Geoffrey Spear]

* Bump dev version number; move a private function to a public helper instead. [Geoffrey Spear]

* Flake8: some whitespace issues introduced in refactor. [Geoffrey Spear]

* Report bad report type earlier (doesn't make sense to do it within a loop over all the lines of the report.) [Geoffrey Spear]

  Refactor parse_generic to reduce complexity, break things out into smaller functions. Fixes issue #20

* Enforce PEP8 import order. [Geoffrey Spear]

* Load version.py relative to setup.py. Fixes bug #19. [Geoffrey Spear]

* Delete pointless never-updated changelog file. [Geoffrey Spear]

* Pep8: missing newline. [Geoffrey Spear]

* Pep8: too many blank lines. [Geoffrey Spear]

* Move format_stat function to pycounter.helpers module. [Geoffrey Spear]

* Bump version for development. [Geoffrey Spear]

  remove deprecated line argument to constructors; we no longer support passing a line of COUNTER 3-compatible data instead of parsed data.

  remove pyisbn requirement that we apparently weren't using.


## 0.9 (2015-12-01)

### Other

* Bump version for release. [Geoffrey Spear]

* Pylint: disable bad-continuation; it disagrees with PEP 8 about the proper place to put closing brackets. (bug reported at https://bitbucket.org/logilab/pylint/issues/638/false-positive-bad-continuation-error ) [Geoffrey Spear]

* Sushiclient: default start and end dates correctly. [Geoffrey Spear]

* Deprecation warnings for passing in a COUNTER 3 data line; reformat docs a bit. [Geoffrey Spear]

* Pylint: disable no-value-for-parameter in click-decorated function (arguments get sent with click magic) [Geoffrey Spear]

  add note about sushiclient to README

* Include class members in autodoc... [Geoffrey Spear]

* Sushiclient: allow output file name to be specified on the command line. [Geoffrey Spear]

* Flake8: 2 errors fixed. [Geoffrey Spear]

* Working code for SUSHI client (sort of, still doesn't set default dates the way it claims...) [Geoffrey Spear]

* Reformat sushiclient docs a bit. Adding missing newline to the end of a file. [Geoffrey Spear]

* Start of command-line sushiclient interface (Doesn't actually do anything yet) [Geoffrey Spear]

* Remove debugging print. [Geoffrey Spear]

* Merge pull request #18 from pitthsls/sushiclient. [Geoffrey Spear]

  use single branch; having sushiclient branch is becoming annoying.

* Module still not on sys.path. [Geoffrey Spear]

* Need to modify sys.path before the import for version, not after... (Doc build was failing on RTD without notifying me... should probably look into that...) [Geoffrey Spear]

* Use pep8 from pypi; nightly is an allowed failure now anyway. [Geoffrey Spear]

  Add an example to README for export to TSV

* Pin lxml version to 3.4.4 for now; 3.5 won't build on the version of PyPy Travis CI is using ( https://github.com/travis-ci/travis-ci/issues/5130 ) [Geoffrey Spear]

* Add beginnings of entry point for a SUSHI client (doesn't do anything yet) [Geoffrey Spear]

* Rename some local variables. [Geoffrey Spear]

* Document a parameter. Bump version and add a module docstring. [Geoffrey Spear]

* Pin openpyxl to &lt; 2.3, since bug affecting pypy was introduced. [Geoffrey Spear]

* Tox needs to install mock library too. [Geoffrey Spear]

* Include pylintrc in MANIFEST.in. [Geoffrey Spear]

* Code Quality: bunch of changes to make pylint happier. [Geoffrey Spear]

* Add MANIFEST.in and check it in CI. [Geoffrey Spear]

* Allow failures on pypy3 and 3.6; lxml having problems on both. [Geoffrey Spear]

* Run tests on pypy3; get pep8 from github since releasaed version doesn't work on Python 3.6. [Geoffrey Spear]

* Test on 3.6. [Geoffrey Spear]

* Trove classifier for Python 3.5 now that it's released. [Geoffrey Spear]

* Coverage; cover sushi_dump codepath. [Geoffrey Spear]

* Using released Python 3.5. [Geoffrey Spear]

* Switch from dateutil to arrow (a newer library with a cleaner, more pythonic interface) [Geoffrey Spear]

* Unix line endings for new file... [Geoffrey Spear]

* Minor reformatting. [Geoffrey Spear]

* Pep8: newline at end of file. [Geoffrey Spear]

* Test coverage for SUSHI error; change exception to generic SushiException instead of AttributeError (although we should look for specific exceptions reported by SUSHI instead... [Geoffrey Spear]

* Post-release version bump back to dev. [Geoffrey Spear]


## 0.8 (2015-08-12)

### Other

* Update to non-dev version number for release. [Geoffrey Spear]

* Merge commit '98e984a' [Geoffrey Spear]

* On pypy, apparently trying to use an lxml.objectify.IntElement directly as an integer doesn't work. [Geoffrey Spear]

* Missing newline at end of constants.py. [Geoffrey Spear]

* Get PDF and HTML data from SUSHI reports. Fixes issue #16. [Geoffrey Spear]

* This needs a None check (although line is close to being removed anyway...) [Geoffrey Spear]

* A bit of reorganization; move constants to their own module. [Geoffrey Spear]

* Remove obsolete directive in .coveragerc; the skipped file no longer exists. [Geoffrey Spear]

* Pass attributes directly into the constructor instead of manually setting them on the report object, since this is possible now that the constructor isn't awful... [Geoffrey Spear]

* For completeness, add report codes for 4 more types of (currently unsupported) reports. [Geoffrey Spear]

* Add an institutional identifier to JR1 as a horrible kludge to get around new csv quoting behavior in 3.5 beta (Completely blank line no longer gets quotes by default; there's really no legitimate reason to have a blank line here anyway) [Geoffrey Spear]

* Store journal DOI and proprietary ID for journal reports... [Geoffrey Spear]

* CSV helper: use UNIX line endings by default; test writing TSV. [Geoffrey Spear]

* Fix spacing of COUNTER reports. [Geoffrey Spear]

* Add total PDF and HTML usage to JR1 report output on totals line. [Geoffrey Spear]

* Update REPORT_DESCRIPTIONS to include all reports NISO knows about. (Note: pycounter doesn't support them all yet...) [Geoffrey Spear]

* Reformat XML. [Geoffrey Spear]

* Include PDF and HTML totals from JR1 reports in data and output. [Geoffrey Spear]

* Openpyxl recent versions check filename extension; to support reading files with arbitrary extensions, we need to just open the file ourself and pass the fd in to load_workbook() [Geoffrey Spear]

* Flake8: missing blank line blows up Travis. [Geoffrey Spear]

* Flake8: missing blank line blows up Travis. [Geoffrey Spear]

* Add file type detection from contents of file, instead of only from filename.  Also add option to explicitly specify filetype. [Geoffrey Spear]

* Test on 3.5-dev, not nightly (which is now 3.6, and breaks flake8) [Geoffrey Spear]

* Fix typo; don't use set comprehension because we support 2.6... [Geoffrey Spear]

* Make flake8 happier. [Geoffrey Spear]

* Beginnings of report output: for JR1 (R4), build table of report data suitable for output to CSV or TSV report. Ref issue #9. [Geoffrey Spear]


## 0.7.1 (2015-07-16)

### Other

* Bump version to 0.7.1 for doc change. [Geoffrey Spear]

* Typo in README for argument names. [Geoffrey Spear]


## 0.7 (2015-06-30)

### Other

* Version 0.7 for release. [Geoffrey Spear]

* Argh still 80 chars. Note to self: fix pyflakes after this. [Geoffrey Spear]

* Use temp variable to make flake8 happy with this line. [Geoffrey Spear]

* Add support for report DB2 (access denied) [Geoffrey Spear]

* Document CounterDatabase. [Geoffrey Spear]

* Add DB1 support to README. [Geoffrey Spear]

* Fix pyflakes error. [Geoffrey Spear]

* Support for DB1 report. ref issue #2. [Geoffrey Spear]

* Lookup table for report codes, instead of using first letter + &quot;R&quot; (DB reports don't follow this pattern) [Geoffrey Spear]

* Add (failing) tests for DB report 1. [Geoffrey Spear]

* Style: missing newlines at end of 2 files; add flake8 to Travis. [Geoffrey Spear]

* Get title, platform, publisher earlier in process and pass to constructor instead of taking from line (further phasing out line parsing deeper in objects) [Geoffrey Spear]

* Use shields.io pypi badge. [Geoffrey Spear]


## 0.6 (2015-04-29)

### Other

* Set more parameters in constructors; moving away from line-based constructing... [Geoffrey Spear]

* Merge branch 'issue1' [Geoffrey Spear]

* Style check; also actually use issn and eissn if passed in... [Geoffrey Spear]

* Refactor: move date helper functions from private functions in report to a new helpers module. [Geoffrey Spear]

* Remove pypip.in image. [Geoffrey Spear]

  pypip.in looks like it's disappeared ( https://github.com/badges/pypipins/issues/37 ), just removing image

* Merge pull request #13 from pitthsls/issue1. [Geoffrey Spear]

  pull in fix for issue 1 (closes issue #1 )

* Pass tuples of date and usage into CounterJournal constructor from SUSHI; fixes issue #1 (still kludgy, since still involves passing bogus COUNTER 3 line into constructor to get title, publisher, etc.) [Geoffrey Spear]

* Failing test for issue 1 (also fix date range on other SUSHI XML test file...) [Geoffrey Spear]

* Bump version number. [Geoffrey Spear]

* (dropped alpha from version number) [Geoffrey Spear]


## 0.5 (2015-04-17)

### Other

* Add some information about lxml installation  to README. Bump version to 0.5 (so pip won't complain about it not being a released version). Fixes issue #12. [Geoffrey Spear]

* Use a pycounter exception rather than a generic one when there's an XML syntax error. [Geoffrey Spear]

* Fix 2 typos in exception docstrings. [Geoffrey Spear]

* Fix RTD link in README. [Geoffrey Spear]

* DOCS: manually structure docs; fix some internal links. [Geoffrey Spear]

* DOCS: remove test suite from API docs; this is just clutter; you'd need to read the source for these to be useful at all. [Geoffrey Spear]

* DOCS: needed to escape backslashes to get tab literal to show up correctly in rendered docs. [Geoffrey Spear]

* Remove CounterPublication alias; was just there for backward compatibility for 1 external tool. [Geoffrey Spear]

* Allow setting all CounterReport attributes in constructor. [Geoffrey Spear]

* Make docs badge go back to project page, add regular link to documentation. [Geoffrey Spear]

* Add changelog file. [Geoffrey Spear]

* Add support for JR1 GOA and fix a couple of typos. [Geoffrey Spear]

* Use RTD theme; it's automatically used on RTD anyway and might as well look the same on local machine when testing. [Geoffrey Spear]

* Bump version after release. [Geoffrey Spear]

* Remove remaining deprecated features; all HSLS legacy code that was using them is fix fixed, and no reason to inflict them on the public. [Geoffrey Spear]

* Change theme back to &quot;default&quot;; rtd still uses sphinx 1.2 and &quot;classic&quot; isn't available. [Geoffrey Spear]

* Some more documentation changing. [Geoffrey Spear]

* Move inline documentation for instance variables into docstrings instead (should make autodoc look more consistent) [Geoffrey Spear]

* Add author_email to quiet warning. [Geoffrey Spear]

* Remove deprecated year attribute from reports entirely. [Geoffrey Spear]

* A few style cleanups. [Geoffrey Spear]

* Add IRC notification from Travis. [Geoffrey Spear]

* Bump dev version after release. [Geoffrey Spear]

* Make docs link go to docs, not status. [Geoffrey Spear]

* Readthedocs link (badge) [Geoffrey Spear]

* Merge branch 'master' of github.com:pitthsls/pycounter. [Geoffrey Spear]

* Pretty github badges. [Geoffrey Spear]

* Drop pypy3 support for now; lxml won't build and it's a known pypy bug) [Geoffrey Spear]

* Fix coverage command. [Geoffrey Spear]

* Add dist to .gitignore. [Geoffrey Spear]

* Add coveralls. [Geoffrey Spear]

* Use logging; cleanup some deprecated stuff. Bump version number. [Geoffrey Spear]

* Travis sudo false to use container-based infrastructure. [Geoffrey Spear]

* Bump version and add readme to pypi. [Geoffrey Spear]

* Bump version and add readme to pypi. [Geoffrey Spear]

* Fix links to RST format. [Geoffrey Spear]

* Rename readme, license. [Geoffrey Spear]

* Add license information. [Geoffrey Spear]

* Some documentation changes. [Geoffrey Spear]

* Rewrite test suite imports to use actual names (instead of names from legacy code in test suite) [Geoffrey Spear]

* Beginnings of README; make flake8 happier. [Geoffrey Spear]

* Fix tox setup. [Geoffrey Spear]

* Tox.ini needs test requirements; tox doesn't install test reqs from setup.py. [Geoffrey Spear]

* __future__ import in wrong place; style. [Geoffrey Spear]

* Some refactoring to remove pitt-specific stuff and to make setup.py closed to pypa's guide...- [Geoffrey Spear]

* Test actual SUSHI requests (with httmock) [Geoffrey Spear]

* Merged in SUSHI-exceptions (pull request #1) [Geoffrey Spear]

  move back to single branch model

* My pycharm style checkers happy. [Geoffrey Spear]

* Some style things; missing kwarg. [Geoffrey Spear]

* Merge remote-tracking branch 'remotes/origin/master' into SUSHI-exceptions. [Geoffrey Spear]

* Option to dump XML. [Geoffrey Spear]

* Account for optional Reports element wrapping the Report. NOTE: does not support multiple Report elelments within the enclosing Report (yet?) [Geoffrey Spear]

* Another bad vendor data problem. [Geoffrey Spear]

* Some guards against bad reports from bad vendors :( [Geoffrey Spear]

* Bump version; add description. [Geoffrey Spear]

* Move exceptions to new module; add a bunch of SUSHI related exception classes. ref issue #15. [Geoffrey Spear]

* Some documentation and style changes. [Geoffrey Spear]

* Add flake8 to tox (and optional lint env) [Geoffrey Spear]

* Exclude pycounter.py from coverage; it just exists for backwards compatability and warns about deprecation. [Geoffrey Spear]

* Remove debugging print statement. [Geoffrey Spear]

* Report version should be integer, not string. [Geoffrey Spear]

* Simple SUSHI XML; test report parameters. [Geoffrey Spear]

* Start SUSHI unit tests. Ref issue #18. [Geoffrey Spear]

* Style, docs. [Geoffrey Spear]

* Fix incorrect package name for dateutil. [Geoffrey Spear]

* When ItemPublisher isn't given for a SUSHI item, make it blank instead of throwing exception. Fixes bug #16. [Geoffrey Spear]

* Workaround Wiley repeating ItemPerformance by skipping months with non ft_total (note: may break if we get legitimately skipped months; fix would rely on refactoring to get rid of monthdata list entirely. [Geoffrey Spear]

* Use dateutil to parse SUSHI report created dates. [Geoffrey Spear]

* Sushi rewrite, now uses lxml and requests instead of suds. [Geoffrey Spear]

* Build SUSHI requests with lxml; send with requests (breaks _raw_to_full since we now return raw XML) [Geoffrey Spear]

* Remove suds requirement, add requests and lxml. [Geoffrey Spear]

* Add suds logging. [Geoffrey Spear]

* Import schemas, to try to fix broken WSDLs on servers. [Geoffrey Spear]

* Rename argument from wsdlurl to wsdl_url. [Geoffrey Spear]

* Fill in usage numbers from SUSHI; closes issue #11. [Geoffrey Spear]

* Build report from sushi raw data (partial; includes metadata, but not individual publications. [Geoffrey Spear]

* Pep 8. [Geoffrey Spear]

* Don't use context manager in assertRaises; not supported in python 2.6. [Geoffrey Spear]

* For single-year reports where no year was explicitly set, get it from the period. [Geoffrey Spear]

* Tests for monthdata list iterator. Closes issue #13. [Geoffrey Spear]

* Add iterator for CounterEresource objects (currently just uses the monthdata list, which may be a problem for reports with more than 12 months of data) [Geoffrey Spear]

* Some attribute docstrings. [Geoffrey Spear]

* Docstring for year property. [Geoffrey Spear]

* Deprecation warnings. [Geoffrey Spear]

* No year and monthdata attributes for multi-year reports. [Geoffrey Spear]

* Fix test data file. [Geoffrey Spear]

* Add test file for multi-year report, with .period test. [Geoffrey Spear]

* Tests for helper. [Geoffrey Spear]

* Some documentation. [Geoffrey Spear]

* Style (now passes flake8) [Geoffrey Spear]

* Merged issue12 into master. Fixes issue #12. [Geoffrey Spear]

* Fill in customer, inst. id (if available), report date period, and date run on CounterReport objects. [Geoffrey Spear]

* Add new attribute stubs, some failing tests. [Geoffrey Spear]

* Fix repr of CounterBook. [Geoffrey Spear]

* Add metric to book, journal reports. [Geoffrey Spear]

* Fix setup bug; add tox support. [Geoffrey Spear]

* Documentation and style stuff. [Geoffrey Spear]

* Get version by exec instead of import; makes setup runnable before dependencies are installed. [Geoffrey Spear]

* More docs, move version to its own module. [Geoffrey Spear]

* Keep sphinx static/template source directories. [Geoffrey Spear]

* Add some empty documentation. [Geoffrey Spear]

* Further DRY; parse all files with the same function that takes iterators of COUNTER rows. [Geoffrey Spear]

* DRY: refactor parse_csv and parse_tsv into parse_separated. [Geoffrey Spear]

* Mark pycounter.pycounter as deprecated; fix tests to import directly from pycounter.report. [Geoffrey Spear]

* Style issues; now passes flake8. [Geoffrey Spear]

* Merge branch 'master' of bitbucket.org:wooble/pycounter. [Geoffrey Spear]

* Ignore more egg stuff. [Geoffrey Spear]

* Support python 3.3+ with six. Fixes issue #10. [Geoffrey Spear]

* Module docstring. [Geoffrey Spear]

* Use jurko's fork of suds for Py3K support. [Geoffrey Spear]

* Use csvhelper.UnicodeReader for parsing CSV and TSV; fixes bug #8. [Geoffrey Spear]

* Rename pycounter.pycounter to pycounter.report (maintaining aliases for backward compatability); use absolute imports everywhere. [Geoffrey Spear]

* Begin py3k support. [Geoffrey Spear]

* Add basic SUSHI fetch support. [Geoffrey Spear]

* Merge changes from master. [Geoffrey Spear]

* .coveragerc to prevent reporting how much of 3rd party modules we've covered... [Geoffrey Spear]

* Ignore eggs created during testing. [Geoffrey Spear]

* Add (failing) test that all parsers return unicode for strings. Ref issue #8. [Geoffrey Spear]

* Add XLSX support (with unit tests). Fixes issue #7. Requires openpyxl, new dependency... [Geoffrey Spear]

* Book report support, with tests. [Geoffrey Spear]

* Suport for BR1 book title report. Fixes issue #5. [Geoffrey Spear]

* Normalize ISBNs to 13 digit; fixes bug #4. [Geoffrey Spear]

* Add support for COUNTER 4 BR 2. [Geoffrey Spear]

* Add EISSN to CounterBook and ISBN to CounterPublication for compatibility. [Geoffrey Spear]

* EAFP -- plus isdigit check was failing horribly for Bad Vendors who put extra spaces in their CSV. [Geoffrey Spear]

* Unit tests for TSV. [Geoffrey Spear]

* Quick hack TSV support (DRY this in the future; the only difference from CSV handling is literally delimiter...) [Geoffrey Spear]

* Add support for COUNTER 4 CSV files (which technically shouldn't exist, but we got one from AIP Scitation so...). Ref issue #1. [Geoffrey Spear]

* Strip newlines from issns. [Geoffrey Spear]

* Ignore blank lines in stats instead of dying horribly. [Geoffrey Spear]

* Deal with thousands separator, missing HTML/PDF columns. [Geoffrey Spear]

* Ignore .egg-info directory. [Geoffrey Spear]

* Book report, more unit tests. [Geoffrey Spear]

* More robust report type detection. [Geoffrey Spear]

* Some tests. [Geoffrey Spear]

* Package structure. [Geoffrey Spear]

* Setup.py, gitignore. [Geoffrey Spear]



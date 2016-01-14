The sushiclient
===============

pycounter comes with a rudimentary SUSHI command line client.

Invocation
----------
.. program:: sushiclient

sushiclient [OPTIONS] <URL>

.. option:: <URL>

   The SUSHI endpoint/WSDL URL to use

Options:

.. option:: -r, --report

   report name (default JR1)

.. option:: -c, --release

   COUNTER release (default 4)

.. option:: -s, --start_date

   Start Date (default first day of last month) in 'YYYY-MM-DD' format

.. option:: -e, --end_date

   Ending Date (default last day of last month) in 'YYYY-MM-DD' format

.. option:: -i, --requestor_id

   Requestor ID as defined in the SUSHI standard

.. option:: -c, --customer_reference

   Customer reference number as defined in the SUSHI standard

.. option:: -f <format>, --format <format>

   Output format (currently only allows the default, tsv)

.. option:: -o <output_file>, --output_file <output_file>

   Path to write output file to. If file already exists, it will be overwritten.

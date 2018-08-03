pycounter API Docs
==================

pycounter.report module
-----------------------

.. module:: pycounter.report

Commonly-used function
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: parse

Classes
^^^^^^^

.. autoclass:: CounterReport
   :members:

.. autoclass:: CounterEresource
   :members:

.. autoclass:: CounterJournal
   :members:

.. autoclass:: CounterBook
   :members:

.. autoclass:: CounterDatabase
   :members:


Other functions
^^^^^^^^^^^^^^^
These are mostly for internal use by the module, but are available to be
called directly if necessary

.. autofunction:: format_stat
.. autofunction:: parse_generic
.. autofunction:: parse_separated
.. autofunction:: parse_xlsx


pycounter.sushi module
----------------------
.. NOTE::
   Before pycounter 1.1, SUSHI requests were always made with SSL verification
   turned off. The default is now to verify certificates. If you must contact
   a SUSHI server without verification, please use the verify=False argument
   to request() or the --no-ssl-verify flag on sushiclient.

.. module:: pycounter.sushi

Commonly-used function
^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: get_report

Other functions
^^^^^^^^^^^^^^^
.. autofunction:: get_sushi_stats_raw

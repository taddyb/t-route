.. _development:

========================
Development
========================

.. warning::
   This guide assumes you have created your own fork (copy) of T-Route, cloned the repo on your own machine, and built T-route using the ``compiler.sh``

Below you will find general information about setting up a development workflow


Development Guide
-----------------

#. Install the required testing packages::

      pip install -e .[test]

   This installs pytest to run the T-Route testing suite

#. Run the tests::

      pytest

Guidance on how to contribute
-----------------------------

.. mdinclude:: ../../../../contributing.md
   :start-line: 2

.. _user_guide:

==========
User Guide
==========

.. currentmodule:: troute

.. warning::
   This page is a work in progress


.. mdinclude:: ../../../../readme.md
   :end-line: 17

Subpackages
-----------

Below, you can find the complete user guide organized by subpackages

==================  ======================================================
Subpackage          Description
==================  ======================================================
:mod:`kernel`       Fortran modules.
:mod:`config`       Configuration parser for T-Route specific file.
:mod:`network`      Manages network, data assimilation, and routing types.
:mod:`nwm`          Coordinates T-Route’s modules.
:mod:`routing`      Handles flow segment and reservoir routing modules.
==================  ======================================================

.. toctree::
   :caption: User guide
   :maxdepth: 1

   kernel
   config
   network
   nwm
   routing
   bmi


.. _getting_started:

===============
Getting Started
===============

.. warning::
   This page is a work in progress

Linux Dependencies
------------------

.. mdinclude:: ../../../../readme.md
   :start-line: 53
   :end-line: 58

Getting Started
---------------
.. highlight:: shell

The following code goes through how to compile T-Route, and route flows for example data. 
`Note: We assume you are using a virtual env, cloned the T-Route repo, and changed your directory
to the T-Route repo.`

Download Python Dependencies

   pip install -r requirements.txt

Compile Cython code and install modules

   ./compiler.sh

Execute a demonstration test with NHD network

   cd test/LowerColorado_TX
   python3 -m nwm_routing -f -V4 test_AnA_V4_NHD.yaml

Execute a demonstration test with HYFeature network

   cd test/LowerColorado_TX_v4
   python3 -m nwm_routing -f -V4 test_AnA_V4_HYFeature.yaml

To learn more about NHD and HYFeature networks, see the User Guide

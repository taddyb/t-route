troute-network (:mod:`network`)
===============================

.. currentmodule:: troute.network


River Connectivity Network
--------------------------

.. warning::
   This page is a work in progress

:mod:`HYFeaturesNetwork` Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Overview
~~~~~~~~

The :mod:`HYFeaturesNetwork` class is a child of the :mod:`AbstractNetwork` class designed to work around 
the HYFeatures Spec and the NOAA-OWP Enterprise Hydrofabric

Class Description
~~~~~~~~~~~~~~~~~

.. py:class:: HYFeaturesNetwork(supernetwork_parameters, waterbody_parameters, data_assimilation_parameters, restart_parameters, compute_parameters, forcing_parameters, hybrid_parameters, preprocessing_parameters, output_parameters, verbose=False, showtiming=False, from_files=True, value_dict={}, bmi_parameters={})

Example Usage
~~~~~~~~~~~~~

.. highlight:: python

Below is how the class is instantiated, where the parameters are created from the `input_handler()` 
internal function for managing config file reads.

   network = HYFeaturesNetwork(
      supernetwork_parameters,
      waterbody_parameters,
      data_assimilation_parameters,
      restart_parameters,
      compute_parameters,
      forcing_parameters,
      hybrid_parameters,
      preprocessing_parameters,
      output_parameters,
      verbose=True, 
      showtiming=showtiming
   )


:mod:`AbstractNetwork` Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`AbstractNetwork` is an abstract base class that provides a foundation for 
network-based hydrological modeling. It includes methods and properties for:

- Initializing the network
- Managing network connections and waterbodies
- Handling forcing data and initial conditions
- Managing routing schemes
- Processing and organizing network data

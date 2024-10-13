troute-config (:mod:`Config`)
=============================

.. currentmodule:: troute.config



T-Route Config Schema
---------------------

The :mod:`Config(BaseModel)` class 


:mod:`NetworkTopologyParameters`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: python

The following subsection defines variables used in the creation of river
network topology. The class consists of three Pydantic BaseModels:

    preprocessing_parameters: "PreprocessingParameters" = Field(default_factory=dict)
    supernetwork_parameters: "SupernetworkParameters"
    waterbody_parameters: "WaterbodyParameters" = Field(default_factory=dict)

:mod:`ComputeParameters`
^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`OutputParameters`
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`BMIParameters`
^^^^^^^^^^^^^^^^^^^^


:mod:`LoggingParameters`
^^^^^^^^^^^^^^^^^^^^^^^^

These settings are viewing internal T-Route debugging statements.
By default, :mod:`log_level` is set to :mod:`DEBUG` with no :mod:`log_directory` defined. 

.. highlight:: python

These settings can be changed through setting the following in the config file:

    log_parameters:

        showtiming: True

        log_level: INFO

        log_directory: path/to/log_directory

Pydantic (v1) input validation
------------------------------

.. highlight:: python

The following code is an example of how one can validate their inputs meet the T-Route schema requirements::

    custom_input_file = args.custom_input_file

    with open(custom_input_file) as custom_file:
        data = yaml.load(custom_file, Loader=yaml.SafeLoader)
    
    troute_configuration = Config(**data)


Strict Validation
-----------------

.. highlight:: python

Strict validation creates a :mod:`Config` instance that verifies existence of file 
and directory field types. If any do not exist, a `pydantic.ValidationError` is raised.::

    custom_input_file = args.custom_input_file

    with open(custom_input_file) as custom_file:
        data = yaml.load(custom_file, Loader=yaml.SafeLoader)
    
    troute_configuration = Config.with_strict_mode(**data)


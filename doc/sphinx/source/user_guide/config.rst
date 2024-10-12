troute-config (:mod:`Config`)
=============================

.. currentmodule:: troute.config



T-Route Config Schema
----------------

The :mod:`Config(BaseModel)` class 

:mod:`LoggingParameters`
^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`NetworkTopologyParameters`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`ComputeParameters`
^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`OutputParameters`
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`BMIParameters`
^^^^^^^^^^^^^^^^^^^^


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


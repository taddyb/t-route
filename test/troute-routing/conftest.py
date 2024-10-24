import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pytest
import troute.nhd_network as nhd_network
from troute.config import Config
import yaml

@pytest.fixture
def nhd_test_network(validated_config: Any, nhd_test_files: Tuple[Path, Path]):
    path, config = nhd_test_files

    with open(config) as custom_file:
        data = yaml.load(custom_file, Loader=yaml.SafeLoader)
    
    troute_configuration = Config(**data)
    config_dict = troute_configuration.dict()

    # Extract main parameter groups
    log_parameters = config_dict.get('log_parameters', {})
    compute_parameters = config_dict.get('compute_parameters', {})
    network_topology_parameters = config_dict.get('network_topology_parameters', {})
    output_parameters = config_dict.get('output_parameters', {})
    bmi_parameters = config_dict.get('bmi_parameters', {})

    # Extract nested parameters
    preprocessing_parameters = network_topology_parameters.get('preprocessing_parameters', {})
    supernetwork_parameters = network_topology_parameters.get('supernetwork_parameters', {})
    waterbody_parameters = network_topology_parameters.get('waterbody_parameters', {})
    forcing_parameters = compute_parameters.get('forcing_parameters', {})
    restart_parameters = compute_parameters.get('restart_parameters', {})
    hybrid_parameters = compute_parameters.get('hybrid_parameters', {})
    parity_parameters = output_parameters.get('wrf_hydro_parity_check', {})
    data_assimilation_parameters = compute_parameters.get('data_assimilation_parameters', {})

    return {
        'path': path,
        'log_parameters': log_parameters,
        'preprocessing_parameters': preprocessing_parameters,
        'supernetwork_parameters': supernetwork_parameters,
        'waterbody_parameters': waterbody_parameters,
        'compute_parameters': compute_parameters,
        'forcing_parameters': forcing_parameters,
        'restart_parameters': restart_parameters,
        'hybrid_parameters': hybrid_parameters,
        'output_parameters': output_parameters,
        'parity_parameters': parity_parameters,
        'data_assimilation_parameters': data_assimilation_parameters,
        'bmi_parameters': bmi_parameters,
    }


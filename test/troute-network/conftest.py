import pandas as pd
from pathlib import Path
import pytest
import troute.nhd_network as nhd_network
from troute.config import Config

import yaml

@pytest.fixture
def reservoir_ids():
    return [401, 402, 403]

@pytest.fixture
def network_clean():
    return [
        [0, 456, -999, 0],
        [1, 178, 4, 0],
        [2, 394, 0, 0],
        [3, 301, 2, 0],
        [4, 798, 0, 403],
        [5, 679, 4, 403],
        [6, 523, 0, 0],
        [7, 815, 2, 0],
        [8, 841, -999, 0],
        [9, 514, 8, 0],
        [10, 458, 9, 0],
        [11, 832, 10, 0],
        [12, 543, 11, 0],
        [13, 240, 12, 0],
        [14, 548, 13, 0],
        [15, 920, 14, 0],
        [16, 920, 15, 401],
        [17, 514, 16, 401],
        [18, 458, 17, 0],
        [180, 458, 17, 0],
        [181, 458, 180, 0],
        [19, 832, 18, 0],
        [20, 543, 19, 0],
        [21, 240, 16, 401],
        [22, 548, 21, 0],
        [23, 920, 22, 0],
        [24, 240, 23, 0],
        [25, 548, 12, 0],
        [26, 920, 25, 402],
        [27, 920, 26, 402],
        [28, 920, 27, 0],
        [2800, 920, 2700, 0],
    ]

@pytest.fixture
def network_circulars(network_clean):
    return [
        [50, 178, 51, 0],
        [51, 178, 50, 0],
        [60, 178, 61, 0],
        [61, 178, 62, 0],
        [62, 178, 60, 0],
        [70, 178, 71, 0],
        [71, 178, 72, 0],
        [72, 178, 73, 0],
        [73, 178, 70, 0],
        [80, 178, 81, 0],
        [81, 178, 82, 0],
        [82, 178, 83, 0],
        [83, 178, 84, 0],
        [84, 178, 80, 0],
    ] + network_clean

@pytest.fixture
def test_columns():
    return {
        "key": 0,
        "dx": 1,
        "downstream": 2,
        "waterbody": 3,
    }

@pytest.fixture
def reverse_test_columns():
    return {0: "key", 1: "dx", 2: "downstream", 3: "waterbody"}

@pytest.fixture
def expected_connections():
    return {
        0: [],
        1: [4],
        2: [0],
        3: [2],
        4: [0],
        5: [4],
        6: [0],
        7: [2],
        8: [],
        9: [8],
        10: [9],
        11: [10],
        12: [11],
        13: [12],
        14: [13],
        15: [14],
        16: [15],
        17: [16],
        18: [17],
        180: [17],
        181: [180],
        19: [18],
        20: [19],
        21: [16],
        22: [21],
        23: [22],
        24: [23],
        25: [12],
        26: [25],
        27: [26],
        28: [27],
        2800: [],
    }

@pytest.fixture
def expected_rconn():
    return {
        0: [2, 4, 6],
        1: [],
        4: [1, 5],
        2: [3, 7],
        3: [],
        5: [],
        6: [],
        7: [],
        8: [9],
        9: [10],
        10: [11],
        11: [12],
        12: [13, 25],
        13: [14],
        14: [15],
        15: [16],
        16: [17, 21],
        17: [18, 180],
        18: [19],
        180: [181],
        181: [],
        19: [20],
        20: [],
        21: [22],
        22: [23],
        23: [24],
        24: [],
        25: [26],
        26: [27],
        27: [28],
        28: [],
        2800: []
    }

@pytest.fixture
def expected_wbody_connections():
    return {
        4: 403,
        5: 403,
        16: 401,
        17: 401,
        21: 401,
        26: 402,
        27: 402
    }

@pytest.fixture
def test_param_df(network_clean, test_columns):
    df = pd.DataFrame(network_clean)
    df = df.rename(columns=nhd_network.reverse_dict(test_columns))
    df = df.set_index("key")
    return df

@pytest.fixture
def test_terminal_code():
    return -999

@pytest.fixture
def test_waterbody_null_code():
    return 0

@pytest.fixture
def HYFeaturesConfig(validated_config):
    path = Path.cwd() / "test/LowerColorado_TX_v4/"
    config = path / "test_AnA_V4_HYFeature_noDA.yaml"

    with open(config) as custom_file:
        data = yaml.load(custom_file, Loader=yaml.SafeLoader)
    
    troute_configuration = Config(**data)

    config_dict = troute_configuration.dict()

    log_parameters = config_dict.get('log_parameters', {})
    compute_parameters = config_dict.get('compute_parameters', {})
    network_topology_parameters = config_dict.get('network_topology_parameters', {})
    output_parameters = config_dict.get('output_parameters', {})
    bmi_parameters = config_dict.get('bmi_parameters', {})

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

from typing import Any, Dict
import os
from pathlib import Path
import pytest

import troute.nhd_network_utilities_v02 as nnu

def test_build_nhd_forcing_sets(
    nhd_test_network: Dict[str, Any], 
    warmstart_nhd_test: Dict[str, Any],
    qlat_data: Dict[str, Any],
) -> None:
    """Test the creation of forcing file sets for NHD network simulation.
    
    Parameters
    ----------
    nhd_test_network : Dict[str, Any]
        Dictionary containing config network settings
    warmstart_nhd_test : Dict[str, Any]
        Dictionary containing warmstart test data for the nhd network
    qlat_data : Dict[str, Any]
        Dictionary containing expected lateral flow data paths
    """
    path = nhd_test_network["path"]
    forcing_parameters = nhd_test_network["forcing_parameters"]

    t0 = warmstart_nhd_test["t0"]

    cwd = Path.cwd()
    os.chdir(path)
    run_sets = nnu.build_forcing_sets(forcing_parameters, t0)
    os.chdir(cwd)
    
    assert run_sets[0]['qlat_files'] == qlat_data['qlat_files']
    assert run_sets[0]['nts'] == qlat_data['nts']
    assert run_sets[0]['final_timestamp'] == qlat_data['final_timestamp']

    
def test_da_sets(
    nhd_test_network: Dict[str, Any],
    warmstart_nhd_test: Dict[str, Any],
    qlat_data: Dict[str, Any],  
):
    run_sets = [qlat_data]
    t0 = warmstart_nhd_test["t0"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]
    
    da_sets = nnu.build_da_sets(data_assimilation_parameters, run_sets, t0)
    assert len(da_sets[0]["usgs_timeslice_files"]) == 0


def test_parity_sets(
    nhd_test_network: Dict[str, Any],
    qlat_data: Dict[str, Any], 
    nhd_validation_files: Dict[str, Any],
):
    run_sets = [qlat_data]
    parity_parameters = nhd_test_network["parity_parameters"]
    parity_sets = nnu.build_parity_sets(parity_parameters, run_sets)
    assert parity_sets[0]['validation_files'] == nhd_validation_files['validation_files']

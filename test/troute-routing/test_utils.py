from typing import Any, Dict
import os
from pathlib import Path
import pytest

import troute.nhd_network_utilities_v02 as nnu

def test_build_nhd_forcing_sets(
    nhd_test_network: Dict[str, Any], 
    warmstart_nhd_test: Dict[str, Any],
    qlat_data: Dict[str, Any],
) -> Dict[str, Any]:
    """ Create run_sets: sets of forcing files for each loop

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

import pytest
from typing import Dict, Any, List
from pathlib import Path
import os
from troute.HYFeaturesNetwork import HYFeaturesNetwork

def test_build_forcing_sets(
    hyfeatures_test_network: Dict[str, Any],
    hyfeatures_network_object: HYFeaturesNetwork,
    hyfeature_qlat_data: List[Dict[str, Any]]
):
    cwd = Path.cwd()
    path = hyfeatures_test_network["path"]

    os.chdir(path)
    run_sets = hyfeatures_network_object.build_forcing_sets()
    os.chdir(cwd)

    assert run_sets == hyfeature_qlat_data

import os
import pathlib
from pathlib import Path
from typing import Any, Dict

from troute import HYFeaturesNetwork


def test_qlat(hyfeatures_test_network: Dict[str, Any]) -> None:
    """Test lateral flow input by reading CSV forcing files from an instantiated network.

    This test verifies that:
    1. Network properly initializes from config
    2. Forcing files exist in the expected directory
    3. Network can build forcing sets from input files
    4. Network can assemble forcing data into lateral flow arrays

    Parameters
    ----------
    hyfeatures_test_network : Dict[str, Any]
        Configuration dictionary containing network settings:
            - path : str or Path
                Base directory for test data
            - supernetwork_parameters : dict
                Network topology configuration
            - waterbody_parameters : dict
                Lake/reservoir parameters
            - data_assimilation_parameters : dict
                Observation assimilation settings
            - restart_parameters : dict
                Model warm start configuration
            - compute_parameters : dict
                Runtime computation settings
            - forcing_parameters : dict
                Input forcing configuration including:
                    - qlat_input_folder : str or Path
                        Directory containing forcing files
                    - qlat_file_pattern_filter : str
                        Glob pattern matching forcing files
            - hybrid_parameters : dict
                Hybrid routing scheme settings
            - preprocessing_parameters : dict
                Network preprocessing options
            - output_parameters : dict
                Output file settings

    Raises
    ------
    AssertionError
        If any of:
            - No forcing files found matching pattern
            - No forcing sets created
            - No files in first forcing set
            - No lateral flow data assembled
    """
    cwd = Path.cwd()
    os.chdir(hyfeatures_test_network["path"])

    network = HYFeaturesNetwork.HYFeaturesNetwork(
        supernetwork_parameters=hyfeatures_test_network["supernetwork_parameters"],
        waterbody_parameters=hyfeatures_test_network["waterbody_parameters"],
        data_assimilation_parameters=hyfeatures_test_network[
            "data_assimilation_parameters"
        ],
        restart_parameters=hyfeatures_test_network["restart_parameters"],
        compute_parameters=hyfeatures_test_network["compute_parameters"],
        forcing_parameters=hyfeatures_test_network["forcing_parameters"],
        hybrid_parameters=hyfeatures_test_network["hybrid_parameters"],
        preprocessing_parameters=hyfeatures_test_network["preprocessing_parameters"],
        output_parameters=hyfeatures_test_network["output_parameters"],
    )
    qlat_input_folder = pathlib.Path(network.forcing_parameters["qlat_input_folder"])
    all_files = sorted(
        qlat_input_folder.glob(network.forcing_parameters["qlat_file_pattern_filter"])
    )
    assert len(all_files) > 0

    run_sets = network.build_forcing_sets()
    assert len(run_sets) > 0
    assert len(run_sets[0]["qlat_files"]) > 0

    network.assemble_forcings(run_sets[0])
    assert network.qlateral.shape[0] > 0
    os.chdir(cwd)
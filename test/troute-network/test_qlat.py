import os
import pathlib
from typing import Any, Dict

from troute import HYFeaturesNetwork


def test_qlat(HYFeaturesConfig: Dict[str, Any]) -> None:
    """Test lateral flow input by reading CSV forcing files from an instantiated network.
    
    This test verifies that:
    1. Network properly initializes from config
    2. Forcing files exist in the expected directory
    3. Network can build forcing sets from input files
    4. Network can assemble forcing data into lateral flow arrays
    
    Parameters
    ----------
    HYFeaturesConfig : Dict[str, Any]
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
    os.chdir(HYFeaturesConfig["path"])

    network = HYFeaturesNetwork.HYFeaturesNetwork(
        supernetwork_parameters=HYFeaturesConfig["supernetwork_parameters"],
        waterbody_parameters=HYFeaturesConfig["waterbody_parameters"],
        data_assimilation_parameters=HYFeaturesConfig["data_assimilation_parameters"],
        restart_parameters=HYFeaturesConfig["restart_parameters"],
        compute_parameters=HYFeaturesConfig["compute_parameters"],
        forcing_parameters=HYFeaturesConfig["forcing_parameters"],
        hybrid_parameters=HYFeaturesConfig["hybrid_parameters"],
        preprocessing_parameters=HYFeaturesConfig["preprocessing_parameters"],
        output_parameters=HYFeaturesConfig["output_parameters"],
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

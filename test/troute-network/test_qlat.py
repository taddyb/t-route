import pathlib
import os
from pathlib import Path
from troute import HYFeaturesNetwork

def _assemble(network):
    qlat_input_folder = pathlib.Path(network.forcing_parameters['qlat_input_folder'])
    all_files = sorted(qlat_input_folder.glob(network.forcing_parameters['qlat_file_pattern_filter']))
    assert(len(all_files) > 0)

    run_sets = network.build_forcing_sets()
    assert(len(run_sets) > 0)
    assert(len(run_sets[0]['qlat_files']) > 0)

    network.assemble_forcings(run_sets[0], )
    assert(network.qlateral.shape[0] > 0)

def test_read_csv(HYFeaturesConfig):
    os.chdir(HYFeaturesConfig["path"])  # Restore original working directory

    network = HYFeaturesNetwork.HYFeaturesNetwork(
        supernetwork_parameters=HYFeaturesConfig['supernetwork_parameters'],
        waterbody_parameters=HYFeaturesConfig['waterbody_parameters'],
        data_assimilation_parameters=HYFeaturesConfig['data_assimilation_parameters'],
        restart_parameters=HYFeaturesConfig['restart_parameters'],
        compute_parameters=HYFeaturesConfig['compute_parameters'],
        forcing_parameters=HYFeaturesConfig['forcing_parameters'],
        hybrid_parameters=HYFeaturesConfig['hybrid_parameters'],
        preprocessing_parameters=HYFeaturesConfig['preprocessing_parameters'],
        output_parameters=HYFeaturesConfig['output_parameters'],
    )
    _assemble(network)

# def test_read_netcdf():
#     network.forcing_parameters['qlat_file_pattern_filter'] = "*NEXOUT.nc"
#     _assemble()

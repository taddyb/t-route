import pytest
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import os

import pandas as pd

from nwm_routing.preprocess import (
    nwm_network_preprocess,
    nwm_initial_warmstate_preprocess,
    unpack_nwm_preprocess_data,
)

@pytest.fixture
def qlat_data():
    return {
        'qlat_files': [
            '202108231400.CHRTOUT_DOMAIN1',
            '202108231500.CHRTOUT_DOMAIN1',
            '202108231600.CHRTOUT_DOMAIN1',
            '202108231700.CHRTOUT_DOMAIN1',
            '202108231800.CHRTOUT_DOMAIN1',
            '202108231900.CHRTOUT_DOMAIN1',
            '202108232000.CHRTOUT_DOMAIN1',
            '202108232100.CHRTOUT_DOMAIN1',
            '202108232200.CHRTOUT_DOMAIN1',
            '202108232300.CHRTOUT_DOMAIN1',
            '202108240000.CHRTOUT_DOMAIN1',
            '202108240100.CHRTOUT_DOMAIN1',
            '202108240200.CHRTOUT_DOMAIN1',
            '202108240300.CHRTOUT_DOMAIN1',
            '202108240400.CHRTOUT_DOMAIN1',
            '202108240500.CHRTOUT_DOMAIN1',
            '202108240600.CHRTOUT_DOMAIN1',
            '202108240700.CHRTOUT_DOMAIN1',
            '202108240800.CHRTOUT_DOMAIN1',
            '202108240900.CHRTOUT_DOMAIN1',
            '202108241000.CHRTOUT_DOMAIN1',
            '202108241100.CHRTOUT_DOMAIN1',
            '202108241200.CHRTOUT_DOMAIN1',
            '202108241300.CHRTOUT_DOMAIN1'
        ],
        'nts': 288,
        'final_timestamp': datetime(2021, 8, 24, 13, 0)
    }

@pytest.fixture
def nhd_built_test_network(nhd_test_network: Dict[str, Any]) -> Dict[str, Any]:
    path = nhd_test_network["path"]
    preprocessing_parameters = nhd_test_network["preprocessing_parameters"]
    supernetwork_parameters = nhd_test_network["supernetwork_parameters"]
    waterbody_parameters = nhd_test_network["waterbody_parameters"]
    compute_parameters = nhd_test_network["compute_parameters"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]

    # Build routing network data objects. Network data objects specify river 
    # network connectivity, channel geometry, and waterbody parameters.
    cwd = Path.cwd()
    os.chdir(path)
    if preprocessing_parameters.get('use_preprocessed_data', False): 
        
        # get data from pre-processed file
        (
            connections,
            param_df,
            wbody_conn,
            waterbodies_df,
            waterbody_types_df,
            break_network_at_waterbodies,
            waterbody_type_specified,
            link_lake_crosswalk,
            independent_networks,
            reaches_bytw,
            rconn,
            link_gage_df,
            usgs_lake_gage_crosswalk, 
            usace_lake_gage_crosswalk,
            diffusive_network_data,
            topobathy_df,
            refactored_diffusive_domain,
            refactored_reaches,
            unrefactored_topobathy_df,
        ) = unpack_nwm_preprocess_data(
            preprocessing_parameters
        )
    else:
        
        # build data objects from scratch
        (
            connections,
            param_df,
            wbody_conn,
            waterbodies_df,
            waterbody_types_df,
            break_network_at_waterbodies,
            waterbody_type_specified,
            link_lake_crosswalk,
            independent_networks,
            reaches_bytw,
            rconn,
            link_gage_df,
            usgs_lake_gage_crosswalk, 
            usace_lake_gage_crosswalk,
            diffusive_network_data,
            topobathy_df,
            refactored_diffusive_domain,
            refactored_reaches,
            unrefactored_topobathy_df,
        ) = nwm_network_preprocess(
            supernetwork_parameters,
            waterbody_parameters,
            preprocessing_parameters,
            compute_parameters,
            data_assimilation_parameters,
        )
    
    os.chdir(cwd)
    return {
        "path": path,
        "connections": connections, 
        "param_df": param_df,
        "wbody_conn": wbody_conn,
        "waterbodies_df": waterbodies_df,
        "waterbody_types_df": waterbody_types_df,
        "break_network_at_waterbodies": break_network_at_waterbodies,
        "waterbody_type_specified": waterbody_type_specified,
        "link_lake_crosswalk": link_lake_crosswalk,
        "independent_networks": independent_networks,
        "reaches_bytw": reaches_bytw,
        "rconn": rconn,
        "link_gage_df": link_gage_df,
        "usgs_lake_gage_crosswalk": usgs_lake_gage_crosswalk, 
        "usace_lake_gage_crosswalk": usace_lake_gage_crosswalk,
        "diffusive_network_data": diffusive_network_data,
        "topobathy_df": topobathy_df,
        "refactored_diffusive_domain": refactored_diffusive_domain,
        "refactored_reaches": refactored_reaches,
        "unrefactored_topobathy_df": unrefactored_topobathy_df,
    }

@pytest.fixture
def warmstart_nhd_test(nhd_test_network: Dict[str, Any], nhd_built_test_network: Dict[str, Any]) -> Dict[str, Any]:
    restart_parameters = nhd_test_network["restart_parameters"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]

    path = nhd_built_test_network["path"]
    param_df = nhd_built_test_network["param_df"]
    waterbodies_df = nhd_built_test_network["waterbodies_df"]
    break_network_at_waterbodies = nhd_built_test_network["break_network_at_waterbodies"]
    link_lake_crosswalk = nhd_built_test_network["link_lake_crosswalk"]
    diffusive_network_data = nhd_built_test_network["diffusive_network_data"]
    
    # list of all segments in the domain (MC + diffusive)
    segment_index = param_df.index
    if diffusive_network_data:
        for tw in diffusive_network_data:
            segment_index = segment_index.append(
                pd.Index(diffusive_network_data[tw]['mainstem_segs'])
            ) 

    waterbodies_df, q0, t0, lastobs_df, da_parameter_dict = nwm_initial_warmstate_preprocess(
        break_network_at_waterbodies,
        restart_parameters,
        data_assimilation_parameters,
        segment_index,
        waterbodies_df,
        link_lake_crosswalk,
    )

    return {
        "path": path,
        "waterbodies_df": waterbodies_df,
        "q0": q0, 
        "t0": t0, 
        "lastobs_df": lastobs_df, 
        "da_parameter_dict":  da_parameter_dict, 
    }


# def route_inputs_nhd_test(nhd_test_network: Dict[str, Any], nhd_built_test_network: Dict[str, Any]) -> Dict[str, Any]:
#     forcing_parameters = nhd_test_network["forcing_parameters"]
#     compute_parameters = nhd_test_network["compute_parameters"]
#     output_parameters = nhd_test_network["output_parameters"] 
#     parity_parameters = nhd_test_network["parity_parameters"]
#     data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]

#     t0 = warmstart_nhd_test["t0"]

#     # Create run_sets: sets of forcing files for each loop
#     run_sets = nnu.build_forcing_sets(forcing_parameters, t0)

#     # Create da_sets: sets of TimeSlice files for each loop
#     if "data_assimilation_parameters" in compute_parameters:
#         da_sets = nnu.build_da_sets(data_assimilation_parameters, run_sets, t0)
        
#     # Create parity_sets: sets of CHRTOUT files against which to compare t-route flows
#     if "wrf_hydro_parity_check" in output_parameters:
#         parity_sets = nnu.build_parity_sets(parity_parameters, run_sets)
#     else:
#         parity_sets = []
    
#     parallel_compute_method = compute_parameters.get("parallel_compute_method", None)
#     subnetwork_target_size = compute_parameters.get("subnetwork_target_size", 1)
#     cpu_pool = compute_parameters.get("cpu_pool", None)
#     qts_subdivisions = forcing_parameters.get("qts_subdivisions", 1)
#     compute_kernel = compute_parameters.get("compute_kernel", "V02-caching")
#     assume_short_ts = compute_parameters.get("assume_short_ts", False)
#     return_courant = compute_parameters.get("return_courant", False)

#     (
#         qlats, 
#         usgs_df, 
#         reservoir_usgs_df, 
#         reservoir_usgs_param_df,
#         reservoir_usace_df,
#         reservoir_usace_param_df,
#         coastal_boundary_depth_df
#     ) = nwm_forcing_preprocess(
#         run_sets[0],
#         forcing_parameters,
#         hybrid_parameters,
#         da_sets[0] if data_assimilation_parameters else {},
#         data_assimilation_parameters,
#         break_network_at_waterbodies,
#         segment_index,
#         link_gage_df,
#         usgs_lake_gage_crosswalk, 
#         usace_lake_gage_crosswalk,
#         link_lake_crosswalk,
#         lastobs_df.index,
#         cpu_pool,
#         t0,
#     )
    
        
#     if showtiming:
#         forcing_end_time = time.time()
#         task_times['forcing_time'] += forcing_end_time - ic_end_time

#     logFileName = 'kernelTalks.log'

#     kernelTalks = log_parameters.get("log_directory", None)

#     if (kernelTalks):

#         logFileName = kernelTalks+'/'+logFileName

#         with open(logFileName, 'w') as preRunLog:
#             preRunLog.write("************************************************************\n") 
#             preRunLog.write("Pre- and post run parameter and run statistics output file. \n") 
#             preRunLog.write("************************************************************\n")     
#         preRunLog.close()

#     # Pass empty subnetwork list to nwm_route. These objects will be calculated/populated
#     # on first iteration of for loop only. For additional loops this will be passed
#     # to function from inital loop. 
#     subnetwork_list = [None, None, None]

#     # Flag for first run for param output
#     firstRun = True
#     # Disable in case there is no log file
#     if (not kernelTalks):
#         firstRun = False

#     for run_set_iterator, run in enumerate(run_sets):

#         t0 = run.get("t0")
#         dt = run.get("dt")
#         nts = run.get("nts")

#         if parity_sets:
#             parity_sets[run_set_iterator]["dt"] = dt
#             parity_sets[run_set_iterator]["nts"] = nts

#         if showtiming:
#             route_start_time = time.time()

import pytest
from typing import Any, Dict
import os
from pathlib import Path

from nwm_routing.preprocess import (
    nwm_forcing_preprocess,
)

def test_nhd_preprocess(
    nhd_test_network: Dict[str, Any], 
    nhd_built_test_network: Dict[str, Any], 
    warmstart_nhd_test: Dict[str, Any],
    qlat_data: Dict[str, Any],
    nhd_validation_files: Dict[str, Any],
):
    path = nhd_test_network["path"]
    forcing_parameters = nhd_test_network["forcing_parameters"]
    hybrid_parameters = nhd_test_network["hybrid_parameters"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]
    compute_parameters = nhd_test_network["compute_parameters"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]
    segment_index = nhd_built_test_network["param_df"].index
    link_gage_df = nhd_built_test_network["link_gage_df"]
    usgs_lake_gage_crosswalk = nhd_built_test_network["usgs_lake_gage_crosswalk"]
    usace_lake_gage_crosswalk = nhd_built_test_network["usace_lake_gage_crosswalk"]
    link_lake_crosswalk = nhd_built_test_network["link_lake_crosswalk"]

    run_sets = [qlat_data]
    da_sets = [{"usgs_timeslice_files": []}]

    t0 = warmstart_nhd_test["t0"]
    lastobs_df = warmstart_nhd_test["lastobs_df"]

    break_network_at_waterbodies = nhd_built_test_network["break_network_at_waterbodies"]

    cpu_pool = compute_parameters.get("cpu_pool", None)

    cwd = Path.cwd()
    os.chdir(path)
    (
        qlats, 
        usgs_df, 
        reservoir_usgs_df, 
        reservoir_usgs_param_df,
        reservoir_usace_df,
        reservoir_usace_param_df,
        coastal_boundary_depth_df
    ) = nwm_forcing_preprocess(
        run_sets[0],
        forcing_parameters,
        hybrid_parameters,
        da_sets[0] if data_assimilation_parameters else {},
        data_assimilation_parameters,
        break_network_at_waterbodies,
        segment_index,
        link_gage_df,
        usgs_lake_gage_crosswalk, 
        usace_lake_gage_crosswalk,
        link_lake_crosswalk,
        lastobs_df.index,
        cpu_pool,
        t0,
    )
    os.chdir(cwd)
    print(qlats)

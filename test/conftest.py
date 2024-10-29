import os
from argparse import Namespace
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd
import pytest
import yaml
from nwm_routing.__main__ import _handle_args_v03
from nwm_routing.input import _input_handler_v03, _input_handler_v04
from nwm_routing.preprocess import (nwm_initial_warmstate_preprocess,
                                    nwm_network_preprocess,
                                    unpack_nwm_preprocess_data)
from pydantic import ValidationError
from troute.config import Config


@pytest.fixture
def qlat_data():
    return {
        "qlat_files": [
            "202108231400.CHRTOUT_DOMAIN1",
            "202108231500.CHRTOUT_DOMAIN1",
            "202108231600.CHRTOUT_DOMAIN1",
            "202108231700.CHRTOUT_DOMAIN1",
            "202108231800.CHRTOUT_DOMAIN1",
            "202108231900.CHRTOUT_DOMAIN1",
            "202108232000.CHRTOUT_DOMAIN1",
            "202108232100.CHRTOUT_DOMAIN1",
            "202108232200.CHRTOUT_DOMAIN1",
            "202108232300.CHRTOUT_DOMAIN1",
            "202108240000.CHRTOUT_DOMAIN1",
            "202108240100.CHRTOUT_DOMAIN1",
            "202108240200.CHRTOUT_DOMAIN1",
            "202108240300.CHRTOUT_DOMAIN1",
            "202108240400.CHRTOUT_DOMAIN1",
            "202108240500.CHRTOUT_DOMAIN1",
            "202108240600.CHRTOUT_DOMAIN1",
            "202108240700.CHRTOUT_DOMAIN1",
            "202108240800.CHRTOUT_DOMAIN1",
            "202108240900.CHRTOUT_DOMAIN1",
            "202108241000.CHRTOUT_DOMAIN1",
            "202108241100.CHRTOUT_DOMAIN1",
            "202108241200.CHRTOUT_DOMAIN1",
            "202108241300.CHRTOUT_DOMAIN1",
        ],
        "nts": 288,
        "final_timestamp": datetime(2021, 8, 24, 13, 0),
    }

@pytest.fixture
def nhd_validation_files():
    files = [
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
    ]
    return {'validation_files': files}

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
    if preprocessing_parameters.get("use_preprocessed_data", False):
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
        ) = unpack_nwm_preprocess_data(preprocessing_parameters)
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
def warmstart_nhd_test(
    nhd_test_network: Dict[str, Any], nhd_built_test_network: Dict[str, Any]
) -> Dict[str, Any]:
    restart_parameters = nhd_test_network["restart_parameters"]
    data_assimilation_parameters = nhd_test_network["data_assimilation_parameters"]

    path = nhd_built_test_network["path"]
    param_df = nhd_built_test_network["param_df"]
    waterbodies_df = nhd_built_test_network["waterbodies_df"]
    break_network_at_waterbodies = nhd_built_test_network[
        "break_network_at_waterbodies"
    ]
    link_lake_crosswalk = nhd_built_test_network["link_lake_crosswalk"]
    diffusive_network_data = nhd_built_test_network["diffusive_network_data"]

    # list of all segments in the domain (MC + diffusive)
    segment_index = param_df.index
    if diffusive_network_data:
        for tw in diffusive_network_data:
            segment_index = segment_index.append(
                pd.Index(diffusive_network_data[tw]["mainstem_segs"])
            )

    waterbodies_df, q0, t0, lastobs_df, da_parameter_dict = (
        nwm_initial_warmstate_preprocess(
            break_network_at_waterbodies,
            restart_parameters,
            data_assimilation_parameters,
            segment_index,
            waterbodies_df,
            link_lake_crosswalk,
        )
    )

    return {
        "path": path,
        "waterbodies_df": waterbodies_df,
        "q0": q0,
        "t0": t0,
        "lastobs_df": lastobs_df,
        "da_parameter_dict": da_parameter_dict,
    }


@contextmanager
def temporarily_change_dir(path: Path):
    """Temporarily changes the current working directory

    This context manager changes the current working directory to the specified path,
    yields control back to the caller, and then changes back to the original directory
    when exiting the context

    Parameters
    ----------
    path : Path
        The path to temporarily change the current working directory to

    Yields
    ------
    None
    """
    original_cwd = Path.cwd()
    if original_cwd != path:
        os.chdir(path)
    try:
        yield
    finally:
        if original_cwd != path:
            os.chdir(original_cwd)


@pytest.fixture
def nhd_test_files() -> Tuple[Path, Path]:
    path = Path.cwd() / "test/LowerColorado_TX/"
    if path.exists() is False:
        print(Path.cwd())
        if "test/LowerColorado_TX/" in Path.cwd().__str__():
            path = Path.cwd()
        elif "test" in Path.cwd().__str__():
            path = Path.cwd() / "LowerColorado_TX/"
        else:
            raise AssertionError("Cannot find NHD test case")
    config = path / "test_AnA_V4_NHD.yaml"

    return path, config


@pytest.fixture
def hyfeatures_test_data() -> Tuple[Path, Path]:
    path = Path.cwd() / "test/LowerColorado_TX_v4/"
    config = path / "test_AnA_V4_HYFeature_noDA.yaml"
    return path, config


@pytest.fixture
def validated_config():
    def _validate_and_fix_config(
        config_path: Path, config_data: Dict[str, Any], strict: bool = True
    ):
        """
        Validates a config, fixes relative paths, and returns the Config object

        Parameters
        ----------
        config_path : Path
            Path to the config file
        config_data : Dict[str, Any]
            Dictionary containing the parsed config data
        strict : bool, optional
            Whether to use strict validation mode, by default True

        Returns
        -------
        Config
            Validated Config object with corrected paths

        Raises
        ------
        ValidationError
            If the config fails validation after path correction attempts
        """
        # Deep copy to avoid modifying the original data
        data = deepcopy(config_data)
        parent_path = config_path.parent

        # First attempt at validation
        try:
            with temporarily_change_dir(parent_path):
                return Config.with_strict_mode(**data) if strict else Config(**data)
        except ValidationError as e:
            # Check for path-related errors and try to fix them
            path_fixed = False
            for error in e.errors():
                if error["type"] == "value_error.path.not_exists":
                    keys = error["loc"]
                    invalid_path = error["ctx"]["path"]
                    corrected_path = Path(parent_path, invalid_path).__str__()

                    # Only fix the path if it actually exists at the corrected location
                    if Path(corrected_path).exists():
                        current = data
                        for key in keys[:-1]:
                            current = current.setdefault(key, {})
                        current[keys[-1]] = corrected_path
                        path_fixed = True

            # If we fixed any paths, try validation again
            if path_fixed:
                with temporarily_change_dir(parent_path):
                    return Config.with_strict_mode(**data) if strict else Config(**data)

            # If we get here, either no paths needed fixing or fixing didn't help
            raise

    return _validate_and_fix_config


@pytest.fixture
def hyfeatures_test_network(hyfeatures_test_data: Tuple[Path, Path]) -> Dict[str, Any]:
    """
    Creates a configuration dictionary for HYFeatures testing.

    Parameters
    ----------
    validated_config : Any
        Configuration validation function
    hyfeatures_test_data: Tuple[Path, Path]
        A tuple containing:
        - path: the path to the test dir
        - config: the config file we want to use

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - path: Path to configuration directory
        - log_parameters: Logging configuration
        - preprocessing_parameters: Network preprocessing settings
        - supernetwork_parameters: Network topology settings
        - waterbody_parameters: Waterbody configuration
        - compute_parameters: Computation settings
        - forcing_parameters: Model forcing configuration
        - restart_parameters: Model restart settings
        - hybrid_parameters: Hybrid routing settings
        - output_parameters: Output configuration
        - parity_parameters: Parity check settings
        - data_assimilation_parameters: DA settings
    """
    path, config = hyfeatures_test_data

    args = _handle_args_v03(["-f", (path / config).__str__()])

    cwd = Path.cwd()

    # Changing work dirs to validate the strict mode
    os.chdir(path)
    (
        log_parameters,
        preprocessing_parameters,
        supernetwork_parameters,
        waterbody_parameters,
        compute_parameters,
        forcing_parameters,
        restart_parameters,
        hybrid_parameters,
        output_parameters,
        parity_parameters,
        data_assimilation_parameters,
    ) = _input_handler_v04(args)

    os.chdir(cwd)

    return {
        "path": path,
        "log_parameters": log_parameters,
        "preprocessing_parameters": preprocessing_parameters,
        "supernetwork_parameters": supernetwork_parameters,
        "waterbody_parameters": waterbody_parameters,
        "compute_parameters": compute_parameters,
        "forcing_parameters": forcing_parameters,
        "restart_parameters": restart_parameters,
        "hybrid_parameters": hybrid_parameters,
        "output_parameters": output_parameters,
        "parity_parameters": parity_parameters,
        "data_assimilation_parameters": data_assimilation_parameters,
        # 'bmi_parameters': bmi_parameters,
    }


@pytest.fixture
def nhd_test_network(nhd_test_files: Tuple[Path, Path]) -> Dict[str, Any]:
    path, config = nhd_test_files

    args = _handle_args_v03(["-f", (path / config).__str__()])

    cwd = Path.cwd()
    os.chdir(path)
    (
        log_parameters,
        preprocessing_parameters,
        supernetwork_parameters,
        waterbody_parameters,
        compute_parameters,
        forcing_parameters,
        restart_parameters,
        hybrid_parameters,
        output_parameters,
        parity_parameters,
        data_assimilation_parameters,
    ) = _input_handler_v03(args)
    os.chdir(cwd)

    return {
        "path": path,
        "log_parameters": log_parameters,
        "preprocessing_parameters": preprocessing_parameters,
        "supernetwork_parameters": supernetwork_parameters,
        "waterbody_parameters": waterbody_parameters,
        "compute_parameters": compute_parameters,
        "forcing_parameters": forcing_parameters,
        "restart_parameters": restart_parameters,
        "hybrid_parameters": hybrid_parameters,
        "output_parameters": output_parameters,
        "parity_parameters": parity_parameters,
        "data_assimilation_parameters": data_assimilation_parameters,
    }

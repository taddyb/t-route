import os
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Tuple
import yaml
from argparse import Namespace

import pytest
from pydantic import ValidationError
from troute.config import Config
from nwm_routing.input import _input_handler_v03, _input_handler_v04
from nwm_routing.__main__ import _handle_args_v03


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
        'path': path,
        'log_parameters': log_parameters,
        'preprocessing_parameters': preprocessing_parameters,
        'supernetwork_parameters': supernetwork_parameters,
        'waterbody_parameters': waterbody_parameters,
        'compute_parameters': compute_parameters,
        'forcing_parameters': forcing_parameters,
        'restart_parameters': restart_parameters,
        "hybrid_parameters": hybrid_parameters,
        "output_parameters": output_parameters,
        "parity_parameters": parity_parameters,
        "data_assimilation_parameters": data_assimilation_parameters,
    }

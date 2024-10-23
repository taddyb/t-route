import os
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import pytest
from pydantic import ValidationError
from troute.config import Config


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

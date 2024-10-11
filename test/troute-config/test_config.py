import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Tuple

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


def test_config_validation(config_data: Tuple[Path, Dict[str, Any]]) -> None:
    """Validates all config files contained within the `test/` folder

    Parameters
    ----------
    config_data : Tuple[Path, Dict[str, Any]]
        A tuple containing the path to the config file and the parsed config data
        - The first element is a Path object pointing to the config file
        - The second element is a dictionary containing the parsed config yaml file data.

    Raises
    ------
    pytest.fail
        If a ValidationError occurs during Config creation, this function will
        call pytest.fail with a detailed error message showing the config file that fails

    Notes
    -----
    This test function uses the `temporarily_change_dir` context manager to
    change the working directory before attempting to create the Config object
    """
    path, data = config_data
    with temporarily_change_dir(path.parent):
        try:
            Config(**data)
        except ValidationError as e:
            error_details = "\n".join(
                f"{' -> '.join(map(str, err['loc']))}: {err['msg']}"
                for err in e.errors()
            )
            pytest.fail(f"Validation failed for {path}:\n{error_details}")

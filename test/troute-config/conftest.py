import pytest
import yaml
from pathlib import Path
from typing import Any, List, Dict, Tuple
from _pytest.fixtures import FixtureRequest


def find_config_files() -> List[Path]:
    """Finds all `.yaml` coinfiguration files within the `test/` dir
    
    Returns
    -------
    List[Path]
        A list of Path objects pointing to each valid configuration
    """
    test_dir = Path(__file__).parents[1]
    files = list(test_dir.glob("*/*.yaml"))
    return files


@pytest.fixture(params=find_config_files())
def config_data(request: FixtureRequest) -> Tuple[Path, Dict[str, Any]]:
    """A fixture for loading yaml files into python dictionary mappings

    Parameters
    ----------
    request : FixtureRequest
        The pytest request object, containing the current parameter value

    Returns
    -------
    Tuple[Path, Dict[str, Any]]
        A tuple containing the path to the YAML file and the loaded data as a dictionary
    """
    data = yaml.load(request.param.read_text(), Loader=yaml.Loader)
    return request.param, data

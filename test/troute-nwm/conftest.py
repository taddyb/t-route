import pytest
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture
def expected_nhd_preprocessed_outputs():
    cwd = Path.cwd()
    return {
        'qlats': pd.read_csv(cwd / "test/troute-nwm/sample_outputs/nhd/qlats.csv"),
    }

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def expected_nhd_preprocessed_outputs():
    cwd = Path.cwd()
    return {
        'qlats': pd.read_csv(cwd / "test/troute-nwm/sample_outputs/nhd/qlats.csv"),
    }

@pytest.fixture
def expected_q0():
    cwd = Path.cwd()
    expected_q0 = pd.read_parquet(cwd / "test/troute-nwm/sample_outputs/nhd/q0_nwm_route_results.parquet")
    return expected_q0

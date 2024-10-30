import pandas as pd
import pytest
import os
from pathlib import Path

@pytest.fixture
def q_lateral_hy_features() -> pd.DataFrame:
    cwd = Path.cwd()
    return pd.read_parquet(cwd / "test/troute-routing/data/q_lateral_hy_features.parquet")

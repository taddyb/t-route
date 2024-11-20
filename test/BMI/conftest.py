import sys

import pytest

sys.path.append("src/")
import bmi_reservoirs
import bmi_troute


@pytest.fixture
def bmi_troute():
    return bmi_troute.bmi_troute()

@pytest.fixture
def config_path():
    return "test/BMI/bmi_example.yaml"

import sys
from pathlib import Path

import numpy as np
import pandas as pd

def test_bmi_model_initialization(bmi_troute, config_file):
    bmi_troute.initialize(bmi_cfg_file="bmi_example.yaml")

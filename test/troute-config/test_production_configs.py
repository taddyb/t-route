"""The five configurations production actually runs, exercised as configurations.

They live in ``test/troute_prod_configs`` with the deployment's paths replaced by repo
fixtures. Everything that decides behavior, especially the RFC selection window and the
persistence horizon, is as deployed and is read from the file rather than restated here.
"""
from __future__ import annotations

import shutil
from datetime import timedelta
from pathlib import Path

import pandas as pd
import pytest
import yaml

from troute.config import Config
from troute.DataAssimilation import _read_timeseries_files

_CONFIGS = sorted((Path(__file__).parent.parent / "troute_prod_configs").glob("*.yaml"))
_FIXTURE = next(
    (Path(__file__).parent.parent / "BMI" / "rfc_timeseries").glob("*.RFCTimeSeries.ncdf"),
    None,
)

pytestmark = pytest.mark.skipif(not _CONFIGS, reason="production configs not present")
_IDS = [f.stem.replace("01205500_troute_config_", "") for f in _CONFIGS]


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def _rfc(cfg: dict) -> dict:
    da = cfg["compute_parameters"]["data_assimilation_parameters"]
    return da["reservoir_da"]["reservoir_rfc_da"]


def _redirect(cfg: dict, tmp: Path) -> dict:
    """Resolve the fixture paths against the repo, and send output to a temp dir.

    The configs carry repo relative paths so they can be read from anywhere; nothing
    that decides behavior is touched.
    """
    root = Path(__file__).parent.parent.parent
    sn = cfg["network_topology_parameters"]["supernetwork_parameters"]
    sn["geo_file_path"] = str(root / sn["geo_file_path"])
    rfc = _rfc(cfg)
    rfc["reservoir_rfc_forecasts_time_series_path"] = str(
        root / rfc["reservoir_rfc_forecasts_time_series_path"]
    )
    cfg["compute_parameters"]["forcing_parameters"]["qlat_input_folder"] = str(tmp)
    out = cfg["output_parameters"]
    out["lakeout_output"] = str(tmp)
    out["stream_output"]["stream_output_directory"] = str(tmp)
    return cfg


def _window(t0: pd.Timestamp, lookback: int, offset: int) -> list[str]:
    """The hourly stamps DataAssimilation builds from a config's two window settings."""
    end = t0 + timedelta(hours=offset)
    stamps, d = [], end - timedelta(hours=lookback)
    while d <= end:
        stamps.append(d.strftime("%Y-%m-%d_%H"))
        d += timedelta(hours=1)
    return stamps


def _run_hours(cfg: dict) -> float:
    fp = cfg["compute_parameters"]["forcing_parameters"]
    return fp["nts"] * fp["dt"] / 3600


# ------------------------------------------------------------------ schema

@pytest.mark.parametrize("path", _CONFIGS, ids=_IDS)
def test_every_production_config_parses(path, tmp_path):
    """Guards the schema against tightening under production's feet.

    ``ReservoirRfcParameters`` forbids extra keys so a misspelled policy cannot be
    dropped in silence; that must not reject a config that is already deployed.
    """
    Config(**_redirect(_load(path), tmp_path))


# ------------------------------------------------------------------ the window

@pytest.mark.parametrize("path", _CONFIGS, ids=_IDS)
def test_the_rfc_window_reaches_backward_only(path):
    """offset 0 in every deployed configuration: nothing issued after t0 is eligible.

    The shipped example configs use offset 28, which selects issues dated after t0.
    Production does not, so a run assimilates only what was in hand when it started.
    """
    rfc = _rfc(_load(path))
    assert rfc["reservoir_rfc_forecasts_offset_hours"] == 0
    t0 = pd.Timestamp("2026-07-13 09:00")
    stamps = _window(t0, rfc["reservoir_rfc_forecasts_lookback_hours"], 0)
    assert stamps[-1] == t0.strftime("%Y-%m-%d_%H")


@pytest.mark.parametrize("path", _CONFIGS, ids=_IDS)
def test_the_window_outlasts_the_interval_between_issues(path):
    """Issues arrive every 6 to 24 hours, so a window under 24 h finds none at most
    cycle times. Every deployed configuration uses 28."""
    assert _rfc(_load(path))["reservoir_rfc_forecasts_lookback_hours"] >= 24


@pytest.mark.skipif(_FIXTURE is None, reason="no RFC fixture available")
@pytest.mark.parametrize("path", _CONFIGS, ids=_IDS)
def test_production_settings_select_the_issue_in_hand(path, tmp_path):
    """The deployed window, driven through the real reader against a real file."""
    rfc = _rfc(_load(path))
    shutil.copy(_FIXTURE, tmp_path / _FIXTURE.name)
    t0 = pd.Timestamp(_FIXTURE.name.split(".", 1)[0].replace("_", " ") + ":00:00")
    got = _read_timeseries_files(
        str(tmp_path),
        _window(t0, rfc["reservoir_rfc_forecasts_lookback_hours"],
                rfc["reservoir_rfc_forecasts_offset_hours"]),
        t0,
        t0 + timedelta(days=rfc["reservoir_rfc_forecast_persist_days"]),
    )
    assert set(got["stationId"]) == {_FIXTURE.name.split(".")[2]}


# ------------------------------------------------------------------ the horizon

@pytest.mark.parametrize("path", _CONFIGS, ids=_IDS)
def test_the_horizon_is_only_reachable_in_the_long_configurations(path):
    """``persist_days`` can only act on a run long enough to reach it.

    At 11 days it is inert in the analysis and short range configurations and live in
    long range, which is where a change to the horizon's meaning is observable.
    """
    cfg = _load(path)
    horizon_hours = _rfc(cfg)["reservoir_rfc_forecast_persist_days"] * 24
    reached = _run_hours(cfg) > horizon_hours
    assert reached == ("lr" in path.stem)


def test_the_run_lengths_are_the_nwm_configurations():
    """Pins what each file is, so a renamed or re-timed config is not read as another."""
    hours = {p.stem.replace("01205500_troute_config_", ""): _run_hours(_load(p))
             for p in _CONFIGS}
    assert hours["default_ana"] == pytest.approx(2)
    assert hours["default_sr"] == pytest.approx(17)
    assert hours["default_ext_ana"] == pytest.approx(27)
    assert hours["default_mrb"] == pytest.approx(239)
    assert hours["lr"] == pytest.approx(719)

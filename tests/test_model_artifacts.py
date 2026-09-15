"""Checks that the committed MMM artifacts are consistent and reproduce the reported fit."""
import pickle
from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import r2_score

WAREHOUSE = Path("data/warehouse/version1")


@pytest.fixture(scope="module")
def artifacts():
    with open(WAREHOUSE / "elastic_net.pkl", "rb") as f:
        model_meta = pickle.load(f)
    with open(WAREHOUSE / "adstock_params.pkl", "rb") as f:
        adstock_meta = pickle.load(f)
    df = pd.read_csv(WAREHOUSE / "data_preparation.csv", parse_dates=["semana_inicio"])
    return model_meta, adstock_meta, df


def test_feature_columns_agree_between_artifacts(artifacts):
    model_meta, adstock_meta, df = artifacts
    assert model_meta["feature_cols"] == adstock_meta["feature_cols"]
    assert set(model_meta["feature_cols"]).issubset(df.columns)
    assert set(model_meta["logadstock_cols"]).issubset(model_meta["feature_cols"])


def test_reported_metrics_are_in_expected_range(artifacts):
    model_meta, _, _ = artifacts
    m = model_meta["metrics"]
    assert m["test_r2"] == pytest.approx(0.649, abs=0.005)
    assert m["train_r2"] == pytest.approx(0.773, abs=0.005)
    assert 8 <= m["test_mape"] <= 20
    assert m["delta_r2_placebo"] > 0.05


def test_full_model_fits_the_weekly_series(artifacts):
    model_meta, _, df = artifacts
    model = model_meta["model"]
    X = df[model_meta["feature_cols"]].values
    y = df[model_meta["target_idx"]].values
    assert len(df) == 258
    assert r2_score(y, model.predict(X)) > 0.7
    assert (model.coef_ >= 0).all(), "ElasticNet was fit with positive=True"

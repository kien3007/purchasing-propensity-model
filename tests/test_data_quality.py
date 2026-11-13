"""
Data Quality, Anti-Leakage, and Model Unit Tests.
Executed with pytest to guarantee rigorous pipeline integrity.
"""
import pytest
import numpy as np
import pandas as pd

from src.features.time_windows import generate_point_in_time_labels
from src.features.feature_builder import PointInTimeFeatureExtractor
from src.models.baselines import HeuristicRecencyBaseline, LogisticRegressionBaseline
from src.evaluation.metrics import compute_propensity_metrics, compute_expected_calibration_error


@pytest.fixture
def synthetic_baskets():
    """Create a minimal synthetic basket dataframe for deterministic testing."""
    records = []
    # Household 1 shops every 5 days: Day 10, 15, 20, 25, 30, 35
    for d in [10, 15, 20, 25, 30, 35]:
        records.append({
            "household_key": 1,
            "BASKET_ID": 1000 + d,
            "DAY": d,
            "STORE_ID": 1,
            "basket_spend": 50.0,
            "basket_items": 5,
            "has_perishable": True,
            "inter_trip_days": 5.0,
        })
    # Household 2 shops only once on Day 12
    records.append({
        "household_key": 2,
        "BASKET_ID": 2012,
        "DAY": 12,
        "STORE_ID": 2,
        "basket_spend": 100.0,
        "basket_items": 10,
        "has_perishable": False,
        "inter_trip_days": np.nan,
    })
    return pd.DataFrame(records)


def test_target_labeling_logic(synthetic_baskets):
    """
    Verify binary label Y is strictly 1 if a trip occurs in (t0, t0 + delta_t] and 0 otherwise.
    """
    cutoff = 20
    delta_t = 14
    # Future window is (20, 34]:
    # Household 1 shopped on Day 25 and 30 -> Y = 1
    # Household 2 did not shop -> Y = 0
    labels = generate_point_in_time_labels(
        synthetic_baskets,
        cutoff_day=cutoff,
        delta_t=delta_t,
        all_households=[1, 2, 3],
    )
    
    assert len(labels) == 3
    assert labels.loc[labels["household_key"] == 1, "target"].values[0] == 1
    assert labels.loc[labels["household_key"] == 2, "target"].values[0] == 0
    assert labels.loc[labels["household_key"] == 3, "target"].values[0] == 0


def test_zero_future_leakage_in_features(synthetic_baskets):
    """
    Verify that transactions occurring strictly AFTER t0 NEVER leak into features.
    """
    cutoff = 22
    extractor = PointInTimeFeatureExtractor(
        baskets_df=synthetic_baskets,
        lookback_days=30,
    )
    # Override all_households to [1, 2]
    extractor.all_households = pd.DataFrame({"household_key": [1, 2]})

    feats = extractor.extract_features_for_cutoff(t0=cutoff)

    # For Household 1: latest trip up to Day 22 was Day 20.
    # Therefore, days_since_last_basket must be 22 - 20 = 2.
    # Trips on Day 25, 30, 35 must NOT be seen!
    hh1 = feats[feats["household_key"] == 1].iloc[0]
    assert hh1["days_since_last_basket"] == 2

    # Household 1 made trips on Day 10, 15, 20 (3 trips in past 30 days)
    assert hh1["baskets_count_30d"] == 3
    assert hh1["spend_30d"] == 150.0


def test_baseline_models_predict_proba():
    """
    Verify that baseline models output valid probabilities between [0, 1].
    """
    X = pd.DataFrame({
        "urgency_ratio": [0.2, 0.9, 1.5, 3.0],
        "days_since_last_basket": [2, 10, 20, 45],
        "spend_30d": [50.0, 120.0, 0.0, 0.0],
    })
    y = pd.Series([0, 1, 1, 0])

    heur = HeuristicRecencyBaseline()
    heur.fit(X, y)
    probs_heur = heur.predict_proba(X)
    assert probs_heur.shape == (4, 2)
    assert np.all(probs_heur >= 0.0) and np.all(probs_heur <= 1.0)
    assert np.allclose(probs_heur.sum(axis=1), 1.0)
    # Higher urgency should result in higher propensity
    assert probs_heur[3, 1] > probs_heur[0, 1]

    lr = LogisticRegressionBaseline()
    lr.fit(X, y)
    probs_lr = lr.predict_proba(X)
    assert probs_lr.shape == (4, 2)
    assert np.all(probs_lr >= 0.0) and np.all(probs_lr <= 1.0)


def test_evaluation_metrics_bounds():
    """
    Verify that all metrics are computed within theoretical mathematical bounds.
    """
    y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])
    y_prob = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.3, 0.85, 0.15, 0.65, 0.25])

    metrics = compute_propensity_metrics(y_true, y_prob)
    assert 0.0 <= metrics["pr_auc"] <= 1.0
    assert 0.0 <= metrics["roc_auc"] <= 1.0
    assert 0.0 <= metrics["brier_score"] <= 1.0
    assert 0.0 <= metrics["ece"] <= 1.0
    assert metrics["top_decile_lift"] > 1.0


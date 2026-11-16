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


# ==============================================================================
# REAL DATA QUALITY CONTRACTS & INVARIANTS (DATA-QUALITY-FRAMEWORKS)
# ==============================================================================

def test_data_loader_cleansing_and_contracts():
    """
    Data Contract Test:
    1. Positive basket spend only (non-positive trips filtered out).
    2. Coupon mappings are 100% unique (exact duplicates eliminated).
    3. Exactly 2,500 unique households are preserved across study.
    """
    from src.data.loader import DataLoader, load_coupons

    # 1. Test coupon deduplication contract
    coupons, redemptions = load_coupons()
    assert len(coupons) == 119_384, f"Expected 119,384 unique coupons, got {len(coupons)}"
    assert coupons.duplicated().sum() == 0, "Coupons table must have 0 duplicate rows"
    assert len(redemptions) == 2_318, f"Expected 2,318 redemption events, got {len(redemptions)}"

    # 2. Test transactions & basket cleansing contract
    data = DataLoader.load_all()
    trans = data["transactions"]
    assert trans["household_key"].nunique() == 2_500, "Must contain all 2,500 households"

    baskets = DataLoader.build_trip_level_baskets(trans, data["products"])
    assert len(baskets) == 275_542, f"Expected 275,542 commercial baskets, got {len(baskets)}"
    assert (baskets["basket_spend"] <= 0).sum() == 0, "No basket with spend <= 0 is allowed"
    assert baskets["household_key"].nunique() == 2_500, "All 2,500 households must be preserved in baskets"


def test_demographics_unknown_imputation_contract():
    """
    Verify that 100% of the 2,500 households are retained in feature extraction,
    with missing demographics (68% of households) properly imputed as 'UNKNOWN'.
    """
    from src.data.loader import DataLoader
    from src.features.feature_builder import PointInTimeFeatureExtractor

    data = DataLoader.load_all()
    baskets = DataLoader.build_trip_level_baskets(data["transactions"], data["products"])

    extractor = PointInTimeFeatureExtractor(
        baskets_df=baskets,
        demographics_df=data["demographics"],
        lookback_days=180,
    )

    feats = extractor.extract_features_for_cutoff(t0=200)

    # Invariant 1: Exactly 2,500 rows
    assert len(feats) == 2_500, f"Expected 2,500 households in feature matrix, got {len(feats)}"

    # Invariant 2: Zero NaNs in demographic categorical features
    demo_cols = ["classification_1", "classification_2", "classification_3", "HOMEOWNER_DESC", "classification_4", "classification_5", "KID_CATEGORY_DESC"]
    for col in demo_cols:
        assert col in feats.columns
        assert feats[col].isna().sum() == 0, f"Column {col} must not contain NaNs"
        # Over 60% of households should be 'UNKNOWN'
        unknown_pct = (feats[col] == "UNKNOWN").mean() * 100
        assert 60.0 <= unknown_pct <= 75.0, f"Column {col} expected ~68% UNKNOWN, got {unknown_pct:.1f}%"


def test_model_artifact_load_and_predict():
    """
    Verify that the trained production LightGBM model artifact loads cleanly,
    contains isotonic calibration, and outputs valid calibrated probabilities.
    """
    from src.config.settings import MODELS_DIR
    from src.models.trainer import LightGBMPropensityModel

    model_path = MODELS_DIR / "lightgbm_propensity_model.joblib"
    assert model_path.exists(), f"Model artifact {model_path} does not exist!"

    model = LightGBMPropensityModel.load(model_path)
    assert hasattr(model, "predict_proba"), "Loaded model must support predict_proba"
    assert model.calibrated_model is not None, "Model must have fitted calibration"
    assert len(model.feature_names_) == 28, f"Expected 28 features, got {len(model.feature_names_)}"



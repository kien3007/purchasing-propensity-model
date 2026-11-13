"""
Model Evaluation and Business Metrics Module.
Calculates PR-AUC, ROC-AUC, Brier Score, ECE, Decile Lift, and Cumulative Gains.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    log_loss,
    precision_recall_curve,
    roc_curve,
)
from sklearn.calibration import calibration_curve
import logging

logger = logging.getLogger(__name__)


def compute_expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """
    Computes Expected Calibration Error (ECE):
    Weighted average difference between predicted confidence and observed accuracy across bins.
    """
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins) - 1
    ece = 0.0
    total_samples = len(y_true)

    for i in range(n_bins):
        mask = bin_indices == i
        bin_count = np.sum(mask)
        if bin_count > 0:
            bin_acc = np.mean(y_true[mask])
            bin_conf = np.mean(y_prob[mask])
            ece += (bin_count / total_samples) * np.abs(bin_acc - bin_conf)

    return float(ece)


def compute_decile_lift(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> pd.DataFrame:
    """
    Computes Decile Lift table:
    Ranks customers by predicted propensity and divides into 10 equal groups.
    Calculates actual conversion rate and lift multiplier for each decile.
    """
    df = pd.DataFrame({"y_true": y_true, "y_prob": y_prob})
    # Rank descending: rank 1 has highest propensity
    df["rank"] = df["y_prob"].rank(ascending=False, method="first")
    df["decile"] = pd.qcut(df["rank"], q=n_bins, labels=[f"Decile {i+1}" for i in range(n_bins)])

    base_rate = float(np.mean(y_true))
    total_positives = int(np.sum(y_true))

    summary = df.groupby("decile", observed=False).agg(
        households=("y_true", "count"),
        actual_buyers=("y_true", "sum"),
        avg_predicted_prob=("y_prob", "mean"),
        actual_response_rate=("y_true", "mean"),
    ).reset_index()

    summary["lift"] = summary["actual_response_rate"] / (base_rate if base_rate > 0 else 1.0)
    summary["cum_buyers"] = summary["actual_buyers"].cumsum()
    summary["cum_gains_pct"] = (summary["cum_buyers"] / (total_positives if total_positives > 0 else 1.0)) * 100.0

    return summary


def compute_propensity_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> Dict[str, Any]:
    """
    Calculates comprehensive statistical and business performance metrics.
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    pr_auc = float(average_precision_score(y_true, y_prob))
    roc_auc = float(roc_auc_score(y_true, y_prob))
    bs = float(brier_score_loss(y_true, y_prob))
    ll = float(log_loss(y_true, y_prob))
    ece = compute_expected_calibration_error(y_true, y_prob)

    base_rate = float(np.mean(y_true))
    # Brier Skill Score relative to predicting the naive base rate
    bs_ref = float(brier_score_loss(y_true, np.full_like(y_prob, base_rate)))
    bss = float(1.0 - (bs / bs_ref)) if bs_ref > 0 else 0.0

    decile_df = compute_decile_lift(y_true, y_prob)
    top_decile_lift = float(decile_df.loc[0, "lift"])
    top_decile_gains = float(decile_df.loc[0, "cum_gains_pct"])
    top_2_deciles_gains = float(decile_df.loc[1, "cum_gains_pct"])

    return {
        "pr_auc": pr_auc,
        "roc_auc": roc_auc,
        "brier_score": bs,
        "brier_skill_score": bss,
        "log_loss": ll,
        "ece": ece,
        "base_rate": base_rate,
        "top_decile_lift": top_decile_lift,
        "top_decile_gains_pct": top_decile_gains,
        "top_2_deciles_gains_pct": top_2_deciles_gains,
        "decile_table": decile_df,
    }

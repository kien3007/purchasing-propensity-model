"""
Baseline Models for Purchase Propensity Benchmarking.
Includes:
1. Heuristic Frequency & Recency Rule (Urgency Ratio)
2. Classical Regularized Logistic Regression (Linear Benchmark)
"""
import numpy as np
import pandas as pd
from typing import Optional, List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)


class HeuristicRecencyBaseline:
    """
    Retail Heuristic Baseline:
    Estimates shopping propensity based on how overdue a household is compared
    to their personal average purchase cycle (Urgency Ratio = Recency / Cadence).

    Formula:
        score = 1 / (1 + exp(-k * (urgency_ratio - 1.0)))
    If urgency_ratio >= 1.0 (they are overdue their usual trip cycle), propensity is high (> 0.5).
    """
    def __init__(self, k: float = 1.5, default_prob: float = 0.5):
        self.k = k
        self.default_prob = default_prob

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        """No parameters to train for heuristic; conforms to scikit-learn API."""
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate calibrated propensity estimates from urgency_ratio.
        """
        if "urgency_ratio" in X.columns:
            urgency = X["urgency_ratio"].fillna(1.0).values
        elif "days_since_last_basket" in X.columns and "avg_days_between_baskets" in X.columns:
            recency = X["days_since_last_basket"].values
            cadence = X["avg_days_between_baskets"].replace(0, np.nan).fillna(14.0).values
            urgency = recency / cadence
        else:
            urgency = np.ones(len(X))

        # Sigmoid response around urgency = 1.0
        # When urgency is high (overdue), propensity increases towards 1.0
        # When urgency is 0 (just shopped today), propensity is lower
        # Bounded between [0.05, 0.95]
        z = self.k * (urgency - 0.8)
        prob_1 = 1.0 / (1.0 + np.exp(-np.clip(z, -10, 10)))
        prob_0 = 1.0 - prob_1
        return np.column_stack([prob_0, prob_1])

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X)[:, 1] >= threshold).astype(int)


class LogisticRegressionBaseline:
    """
    Linear Benchmark:
    Preprocesses numeric features with median imputation and standard scaling,
    followed by L2-regularized Logistic Regression.
    """
    def __init__(self, C: float = 1.0, random_state: int = 42):
        self.C = C
        self.random_state = random_state
        self.pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(
                C=self.C,
                max_iter=1000,
                random_state=self.random_state,
                solver="lbfgs"
            ))
        ])
        self.feature_names_: List[str] = []

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.feature_names_ = list(X.columns)
        self.pipeline.fit(X, y)
        logger.info(f"Fitted Logistic Regression baseline on {len(X):,} samples across {len(self.feature_names_)} features.")
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.pipeline.predict_proba(X)

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X)[:, 1] >= threshold).astype(int)

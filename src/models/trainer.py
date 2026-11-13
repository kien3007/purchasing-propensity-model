"""
Production LightGBM Propensity Model with Calibration and SHAP Explainability.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path
import joblib
import lightgbm as lgb
from sklearn.calibration import CalibratedClassifierCV
import shap

from src.config.settings import model_config, MODELS_DIR

logger = logging.getLogger(__name__)


class LightGBMPropensityModel:
    """
    Gradient Boosted Decision Tree model for household basket propensity.
    Features:
    - Native support for categorical features (demographics).
    - Early stopping on temporal validation split.
    - Post-hoc Isotonic Probability Calibration to ensure realistic probabilities.
    - Native SHAP TreeExplainer integration for business explainability.
    """
    def __init__(
        self,
        n_estimators: int = model_config.n_estimators,
        learning_rate: float = model_config.learning_rate,
        max_depth: int = model_config.max_depth,
        num_leaves: int = model_config.num_leaves,
        min_child_samples: int = model_config.min_child_samples,
        subsample: float = model_config.subsample,
        colsample_bytree: float = model_config.colsample_bytree,
        scale_pos_weight: float = model_config.scale_pos_weight,
        random_state: int = model_config.random_state,
        calibrate: bool = True,
    ):
        self.params = {
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "max_depth": max_depth,
            "num_leaves": num_leaves,
            "min_child_samples": min_child_samples,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "scale_pos_weight": scale_pos_weight,
            "random_state": random_state,
            "objective": "binary",
            "metric": ["binary_logloss", "average_precision"],
            "verbosity": -1,
            "n_jobs": -1,
        }
        self.calibrate = calibrate
        self.model: Optional[lgb.LGBMClassifier] = None
        self.calibrated_model: Optional[CalibratedClassifierCV] = None
        self.feature_names_: List[str] = []
        self.categorical_features_: List[str] = []
        self.explainer: Optional[shap.TreeExplainer] = None

    def _prepare_df(self, X: pd.DataFrame) -> pd.DataFrame:
        """Ensure categorical features are appropriately typed."""
        X_copy = X.copy()
        for col in self.categorical_features_:
            if col in X_copy.columns:
                X_copy[col] = X_copy[col].astype("category")
        return X_copy

    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        categorical_features: Optional[List[str]] = None,
        early_stopping_rounds: int = model_config.early_stopping_rounds,
    ):
        self.feature_names_ = list(X_train.columns)
        self.categorical_features_ = categorical_features or []

        X_tr = self._prepare_df(X_train)
        
        self.model = lgb.LGBMClassifier(**self.params)

        callbacks = []
        eval_set = None
        if X_val is not None and y_val is not None:
            X_v = self._prepare_df(X_val)
            eval_set = [(X_tr, y_train), (X_v, y_val)]
            callbacks.append(lgb.early_stopping(stopping_rounds=early_stopping_rounds, verbose=False))
            callbacks.append(lgb.log_evaluation(period=100))

        logger.info(f"Training LightGBM on {len(X_tr):,} samples with {len(self.feature_names_)} features...")
        self.model.fit(
            X_tr,
            y_train,
            eval_set=eval_set,
            callbacks=callbacks,
        )

        best_iteration = getattr(self.model, "best_iteration_", self.params["n_estimators"])
        logger.info(f"Training completed. Best iteration: {best_iteration}")

        # Post-hoc Probability Calibration
        if self.calibrate and X_val is not None and y_val is not None:
            logger.info("Applying Isotonic Probability Calibration on validation set...")
            self.calibrated_model = CalibratedClassifierCV(
                estimator=self.model,
                method="isotonic",
                cv="prefit",
            )
            self.calibrated_model.fit(self._prepare_df(X_val), y_val)
            logger.info("Calibration successfully fitted.")
        else:
            self.calibrated_model = None

        return self

    def predict_proba(self, X: pd.DataFrame, use_calibrated: bool = True) -> np.ndarray:
        """
        Output calibrated probabilities for class 0 and class 1.
        """
        X_prep = self._prepare_df(X)
        if self.calibrated_model is not None and use_calibrated:
            return self.calibrated_model.predict_proba(X_prep)
        if self.model is not None:
            return self.model.predict_proba(X_prep)
        raise ValueError("Model has not been fitted yet.")

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X)[:, 1] >= threshold).astype(int)

    def get_feature_importances(self, importance_type: str = "gain") -> pd.DataFrame:
        """Extract sorted feature importances (split count or gain)."""
        if self.model is None:
            raise ValueError("Model is not fitted.")
        raw_imp = self.model.booster_.feature_importance(importance_type=importance_type)
        imp_df = pd.DataFrame({
            "feature": self.feature_names_,
            f"importance_{importance_type}": raw_imp,
        }).sort_values(by=f"importance_{importance_type}", ascending=False).reset_index(drop=True)
        return imp_df

    def explain(self, X_sample: pd.DataFrame) -> Tuple[np.ndarray, shap.TreeExplainer]:
        """Compute SHAP values for a sample dataset."""
        if self.model is None:
            raise ValueError("Model is not fitted.")
        X_prep = self._prepare_df(X_sample)
        if self.explainer is None:
            self.explainer = shap.TreeExplainer(self.model)
        shap_values = self.explainer.shap_values(X_prep)
        if isinstance(shap_values, list):
            # Binary classification returns list of [class 0, class 1]
            return shap_values[1], self.explainer
        return shap_values, self.explainer

    def save(self, filepath: Optional[Path] = None):
        """Save model pipeline to disk."""
        target_path = filepath or (MODELS_DIR / "lightgbm_propensity_model.joblib")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "model": self.model,
            "calibrated_model": self.calibrated_model,
            "params": self.params,
            "feature_names": self.feature_names_,
            "categorical_features": self.categorical_features_,
        }, target_path)
        logger.info(f"Model saved to {target_path}")

    @classmethod
    def load(cls, filepath: Optional[Path] = None):
        """Load trained model pipeline from disk."""
        target_path = filepath or (MODELS_DIR / "lightgbm_propensity_model.joblib")
        data = joblib.load(target_path)
        instance = cls()
        instance.model = data["model"]
        instance.calibrated_model = data["calibrated_model"]
        instance.params = data["params"]
        instance.feature_names_ = data["feature_names"]
        instance.categorical_features_ = data["categorical_features"]
        logger.info(f"Model loaded from {target_path}")
        return instance

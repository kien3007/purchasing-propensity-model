"""
End-to-End Training and Evaluation Pipeline.
Loads data, builds Point-in-Time feature matrices, trains baselines & LightGBM,
calibrates probabilities, evaluates on OOT test cutoffs, and outputs performance reports.
"""
import sys
import json
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional
import numpy as np
import pandas as pd

from src.config.settings import time_config, model_config, MODELS_DIR, REPORTS_DIR
from src.data.loader import DataLoader
from src.features.time_windows import generate_point_in_time_labels
from src.features.feature_builder import PointInTimeFeatureExtractor
from src.models.baselines import HeuristicRecencyBaseline, LogisticRegressionBaseline
from src.models.trainer import LightGBMPropensityModel
from src.evaluation.metrics import compute_propensity_metrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("TrainPipeline")


def build_dataset_for_cutoffs(
    extractor: PointInTimeFeatureExtractor,
    baskets_df: pd.DataFrame,
    cutoffs: list,
    delta_t: int = time_config.prediction_window_days,
) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Extracts features and labels for multiple cutoff dates and stacks them.
    Guarantees strict Point-in-Time separation.
    """
    feature_dfs = []
    label_dfs = []

    for t0 in cutoffs:
        logger.info(f"Extracting features and target labels for cutoff DAY = {t0}...")
        f_df = extractor.extract_features_for_cutoff(t0)
        l_df = generate_point_in_time_labels(baskets_df, cutoff_day=t0, delta_t=delta_t)
        
        merged = f_df.merge(l_df[["household_key", "cutoff_day", "target"]], on=["household_key", "cutoff_day"])
        feature_dfs.append(merged)

    full_df = pd.concat(feature_dfs, ignore_index=True)
    
    # Exclude metadata columns from feature matrix
    exclude_cols = ["household_key", "cutoff_day", "target"]
    feature_cols = [c for c in full_df.columns if c not in exclude_cols]
    
    X = full_df[feature_cols]
    y = full_df["target"]
    
    logger.info(f"Built dataset: {len(X):,} rows, {len(feature_cols)} features. Positive target rate: {y.mean()*100:.2f}%")
    return X, y, feature_cols


def run_pipeline():
    logger.info("=== Starting Purchase Propensity Training Pipeline ===")

    # 1. Load Cleaned Data
    data = DataLoader.load_all()
    baskets = DataLoader.build_trip_level_baskets(
        trans_df=data["transactions"],
        product_df=data["products"],
    )

    # Prepare campaigns joined with descriptions
    campaigns = None
    if data["campaigns"] is not None and data["campaign_desc"] is not None:
        campaigns = data["campaigns"].merge(data["campaign_desc"], on="CAMPAIGN", how="inner")

    # 2. Initialize Feature Extractor
    extractor = PointInTimeFeatureExtractor(
        baskets_df=baskets,
        campaigns_df=campaigns,
        redemptions_df=data["redemptions"],
        demographics_df=data["demographics"],
        lookback_days=time_config.observation_window_days,
    )

    # 3. Build Datasets
    logger.info(f"Building Training set across cutoffs: {time_config.train_cutoffs}")
    X_train, y_train, feature_cols = build_dataset_for_cutoffs(
        extractor, baskets, time_config.train_cutoffs, delta_t=time_config.prediction_window_days
    )

    logger.info(f"Building Validation set across cutoffs: {time_config.val_cutoffs}")
    X_val, y_val, _ = build_dataset_for_cutoffs(
        extractor, baskets, time_config.val_cutoffs, delta_t=time_config.prediction_window_days
    )

    logger.info(f"Building Out-Of-Time (OOT) Test set across cutoffs: {time_config.test_cutoffs}")
    X_test, y_test, _ = build_dataset_for_cutoffs(
        extractor, baskets, time_config.test_cutoffs, delta_t=time_config.prediction_window_days
    )

    # Identify categorical columns
    categorical_cols = [
        col for col in feature_cols
        if X_train[col].dtype.name == "category" or str(X_train[col].dtype) == "object"
    ]
    logger.info(f"Identified {len(categorical_cols)} categorical features: {categorical_cols}")

    results = {}

    # 4. Benchmark 1: Heuristic Recency Baseline
    logger.info("Evaluating Baseline 1: Heuristic Recency Rule...")
    heuristic = HeuristicRecencyBaseline()
    heuristic.fit(X_train, y_train)
    y_prob_heur = heuristic.predict_proba(X_test)[:, 1]
    results["Heuristic_Rule"] = compute_propensity_metrics(y_test, y_prob_heur)
    logger.info(
        f"[Heuristic] PR-AUC: {results['Heuristic_Rule']['pr_auc']:.4f} | "
        f"ROC-AUC: {results['Heuristic_Rule']['roc_auc']:.4f} | "
        f"Brier: {results['Heuristic_Rule']['brier_score']:.4f} | "
        f"Top Decile Lift: {results['Heuristic_Rule']['top_decile_lift']:.2f}x"
    )

    # 5. Benchmark 2: Regularized Logistic Regression
    logger.info("Evaluating Baseline 2: Logistic Regression (Numeric Features)...")
    numeric_cols = [c for c in feature_cols if c not in categorical_cols]
    log_reg = LogisticRegressionBaseline()
    log_reg.fit(X_train[numeric_cols], y_train)
    y_prob_lr = log_reg.predict_proba(X_test[numeric_cols])[:, 1]
    results["Logistic_Regression"] = compute_propensity_metrics(y_test, y_prob_lr)
    logger.info(
        f"[LogReg]    PR-AUC: {results['Logistic_Regression']['pr_auc']:.4f} | "
        f"ROC-AUC: {results['Logistic_Regression']['roc_auc']:.4f} | "
        f"Brier: {results['Logistic_Regression']['brier_score']:.4f} | "
        f"Top Decile Lift: {results['Logistic_Regression']['top_decile_lift']:.2f}x"
    )

    # 6. Main Model: LightGBM (Uncalibrated & Calibrated)
    logger.info("Training Main Model: LightGBM GBDT...")
    lgb_model = LightGBMPropensityModel(calibrate=True)
    lgb_model.fit(
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        categorical_features=categorical_cols,
    )

    # Uncalibrated test metrics
    y_prob_lgb_raw = lgb_model.predict_proba(X_test, use_calibrated=False)[:, 1]
    results["LightGBM_Raw"] = compute_propensity_metrics(y_test, y_prob_lgb_raw)

    # Calibrated test metrics
    y_prob_lgb_cal = lgb_model.predict_proba(X_test, use_calibrated=True)[:, 1]
    results["LightGBM_Calibrated"] = compute_propensity_metrics(y_test, y_prob_lgb_cal)

    logger.info(
        f"[LightGBM-Raw] PR-AUC: {results['LightGBM_Raw']['pr_auc']:.4f} | "
        f"ROC-AUC: {results['LightGBM_Raw']['roc_auc']:.4f} | "
        f"Brier: {results['LightGBM_Raw']['brier_score']:.4f} | "
        f"ECE: {results['LightGBM_Raw']['ece']:.4f} | "
        f"Top Decile Lift: {results['LightGBM_Raw']['top_decile_lift']:.2f}x"
    )
    logger.info(
        f"[LightGBM-Cal] PR-AUC: {results['LightGBM_Calibrated']['pr_auc']:.4f} | "
        f"ROC-AUC: {results['LightGBM_Calibrated']['roc_auc']:.4f} | "
        f"Brier: {results['LightGBM_Calibrated']['brier_score']:.4f} | "
        f"ECE: {results['LightGBM_Calibrated']['ece']:.4f} | "
        f"Top Decile Lift: {results['LightGBM_Calibrated']['top_decile_lift']:.2f}x"
    )

    # 7. Feature Importance & SHAP Drivers
    feat_imp = lgb_model.get_feature_importances(importance_type="gain")
    logger.info("Top 10 Most Important Features (Gain):")
    for idx, row in feat_imp.head(10).iterrows():
        logger.info(f"  {idx+1:2d}. {row['feature']:<32} : {row['importance_gain']:>12,.1f}")

    # SHAP summary on a sample of test data
    logger.info("Computing SHAP explanations on test sample...")
    sample_size = min(1000, len(X_test))
    X_sample = X_test.iloc[:sample_size]
    shap_vals, _ = lgb_model.explain(X_sample)
    mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)
    shap_ranking = pd.DataFrame({
        "feature": feature_cols,
        "mean_abs_shap": mean_abs_shap,
    }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)
    
    logger.info("Top 10 SHAP Drivers:")
    for idx, row in shap_ranking.head(10).iterrows():
        logger.info(f"  {idx+1:2d}. {row['feature']:<32} : {row['mean_abs_shap']:>8.4f}")

    # 8. Save Model Pipeline
    model_save_path = MODELS_DIR / "lightgbm_propensity_model.joblib"
    lgb_model.save(model_save_path)

    # 9. Save Evaluation Report
    # Clean decile table for JSON export
    serializable_results = {}
    for model_name, m in results.items():
        serializable_results[model_name] = {
            k: (v.to_dict(orient="records") if isinstance(v, pd.DataFrame) else v)
            for k, v in m.items()
        }

    report_json_path = REPORTS_DIR / "model_performance_summary.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(serializable_results, f, indent=2)
    logger.info(f"Saved evaluation metrics JSON to {report_json_path}")

    # Save Markdown summary report
    markdown_report_path = REPORTS_DIR / "model_performance_summary.md"
    generate_markdown_report(results, feat_imp, shap_ranking, markdown_report_path)
    logger.info(f"Saved evaluation Markdown report to {markdown_report_path}")

    logger.info("=== Purchase Propensity Training Pipeline Complete ===")
    return results


def generate_markdown_report(results, feat_imp, shap_ranking, filepath: Path):
    """Generate executive and technical evaluation report in Markdown."""
    cal = results["LightGBM_Calibrated"]
    raw = results["LightGBM_Raw"]
    lr = results["Logistic_Regression"]
    heur = results["Heuristic_Rule"]

    md = f"""# Purchase Propensity Model - Performance & Benchmark Report

## 1. Executive Summary & Benchmark Comparison (Out-of-Time Test Set)

| Model Architecture | PR-AUC (Precision-Recall) | ROC-AUC | Brier Score (Lower is better) | ECE (Calibration Error) | Top Decile Lift | Top 20% Cumulative Gains |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LightGBM (Isotonic Calibrated)** | **{cal['pr_auc']:.4f}** | **{cal['roc_auc']:.4f}** | **{cal['brier_score']:.4f}** | **{cal['ece']:.4f}** | **{cal['top_decile_lift']:.2f}x** | **{cal['top_2_deciles_gains_pct']:.1f}%** |
| LightGBM (Raw / Uncalibrated) | {raw['pr_auc']:.4f} | {raw['roc_auc']:.4f} | {raw['brier_score']:.4f} | {raw['ece']:.4f} | {raw['top_decile_lift']:.2f}x | {raw['top_2_deciles_gains_pct']:.1f}% |
| Logistic Regression (Linear) | {lr['pr_auc']:.4f} | {lr['roc_auc']:.4f} | {lr['brier_score']:.4f} | {lr['ece']:.4f} | {lr['top_decile_lift']:.2f}x | {lr['top_2_deciles_gains_pct']:.1f}% |
| Heuristic Recency Rule | {heur['pr_auc']:.4f} | {heur['roc_auc']:.4f} | {heur['brier_score']:.4f} | {heur['ece']:.4f} | {heur['top_decile_lift']:.2f}x | {heur['top_2_deciles_gains_pct']:.1f}% |

*Base rate on Out-Of-Time Test set: {cal['base_rate']*100:.2f}%.*

---

## 2. Decile Lift Table (LightGBM Calibrated)

| Decile | Households | Actual Buyers | Predicted Prob | Actual Conversion | Lift vs Base Rate | Cumulative Gains (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for _, row in cal["decile_table"].iterrows():
        md += f"| {row['decile']} | {int(row['households']):,} | {int(row['actual_buyers']):,} | {row['avg_predicted_prob']*100:.1f}% | {row['actual_response_rate']*100:.1f}% | {row['lift']:.2f}x | {row['cum_gains_pct']:.1f}% |\n"

    md += """
---

## 3. Top 10 Feature Importance (Tree Split Gain)

| Rank | Feature Name | Total Gain Importance | Business Interpretation |
| :---: | :--- | :---: | :--- |
"""
    interpretations = {
        "urgency_ratio": "Tỷ lệ quá hạn chu kỳ cá nhân (Recency / Chu kỳ trung vị)",
        "days_since_last_basket": "Số ngày trôi qua kể từ giỏ hàng gần nhất",
        "baskets_count_14d": "Tần suất mua sắm ngắn hạn 14 ngày",
        "baskets_count_30d": "Tần suất mua sắm 30 ngày gần nhất",
        "days_since_last_perishable": "Số ngày kể từ lần mua thực phẩm tươi sống cuối",
        "median_inter_trip": "Chu kỳ mua sắm đặc trưng của hộ gia đình",
        "frequency_momentum_30_vs_90": "Gia tốc tần suất (30 ngày gần đây tăng hay chậm)",
        "spend_30d": "Tổng chi tiêu 30 ngày gần nhất",
        "store_loyalty_index": "Tỷ trọng chi tiêu tại cửa hàng ruột (Độ trung thành)",
        "aov_90d": "Giá trị trung bình mỗi giỏ hàng (AOV)",
        "perishable_basket_ratio_90d": "Tỷ lệ giỏ hàng có đồ tươi sống trong 90 ngày",
    }

    for idx, row in feat_imp.head(10).iterrows():
        feat = row["feature"]
        interp = interpretations.get(feat, "Chỉ số hành vi / nhân khẩu học")
        md += f"| {idx+1} | `{feat}` | {row['importance_gain']:,.1f} | {interp} |\n"

    md += """
---

## 4. Top 10 SHAP Explanations (Mean Absolute SHAP Value)

| Rank | Feature | Mean |SHAP| (Log-odds Impact) |
| :---: | :--- | :---: |
"""
    for idx, row in shap_ranking.head(10).iterrows():
        md += f"| {idx+1} | `{row['feature']}` | {row['mean_abs_shap']:.4f} |\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    run_pipeline()
